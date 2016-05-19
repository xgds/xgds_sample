# __BEGIN_LICENSE__
# Copyright (c) 2015, United States Government, as represented by the
# Administrator of the National Aeronautics and Space Administration.
# All rights reserved.
#
# The xGDS platform is licensed under the Apache License, Version 2.0
# (the "License"); you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
# http://www.apache.org/licenses/LICENSE-2.0.
#
# Unless required by applicable law or agreed to in writing, software distributed
# under the License is distributed on an "AS IS" BASIS, WITHOUT WARRANTIES OR
# CONDITIONS OF ANY KIND, either express or implied. See the License for the
# specific language governing permissions and limitations under the License.
# __END_LICENSE__
from django.contrib.auth.decorators import login_required
from django.shortcuts import render_to_response,  get_object_or_404, redirect
from django.core.urlresolvers import reverse
from django.http import HttpResponseBadRequest, HttpResponse
from django.template import RequestContext
from django.forms.formsets import formset_factory
from django.conf import settings
from django.contrib import messages 
from django.db.models import Max
from django.contrib.auth.models import User
from PyPDF2 import PdfFileMerger, PdfFileReader

import json
import os
import re

from geocamUtil.loader import getClassByName, LazyGetModelByName
from forms import SampleForm
from xgds_data.forms import SearchForm, SpecializedForm
from xgds_sample.models import SampleType, Region, SampleLabelSize
from xgds_core.views import get_handlebars_templates

from geocamUtil.datetimeJsonEncoder import DatetimeJsonEncoder
from django.views.static import serve
from xgds_sample.labels import *

from django.http import HttpResponse
from StringIO import StringIO


SAMPLE_MODEL = LazyGetModelByName(settings.XGDS_SAMPLE_SAMPLE_MODEL)
LABEL_MODEL = LazyGetModelByName(settings.XGDS_SAMPLE_LABEL_MODEL)

XGDS_SAMPLE_TEMPLATE_LIST = list(settings.XGDS_MAP_SERVER_HANDLEBARS_DIRS)
XGDS_SAMPLE_TEMPLATE_LIST = XGDS_SAMPLE_TEMPLATE_LIST + settings.XGDS_CORE_TEMPLATE_DIRS[settings.XGDS_SAMPLE_SAMPLE_MODEL]
    
# get all user names (string)
def getUserNames():
    allUsers = [user.first_name + ' ' + user.last_name  for user in User.objects.all()]
    allUsers = [str(x) for x in allUsers if x.strip()]
    return allUsers


def deleteLabelAndSample(request, labelNum):
    label = LABEL_MODEL.get().objects.get(number=labelNum)
    message = 'Deleted label %d' % label.number
    try:
        message = message + ' and sample %s ' % label.sample.name
        label.sample.delete()
    except:
        pass
    label.delete()
    messages.error(request, message)
    return render_to_response('xgds_sample/recordSample.html',
                              RequestContext(request, {}))
    

@login_required 
def editSample(request, samplePK, form=None):
    if not form:
        sample = SAMPLE_MODEL.get().objects.get(pk=samplePK)
        form = SampleForm(instance=sample)
    return render_to_response('xgds_sample/sampleEdit.html',
                              RequestContext(request, {'form': form,
                                                       'users': getUserNames(),
                                                       'modelName': settings.XGDS_SAMPLE_SAMPLE_KEY,
                                                       'templates': get_handlebars_templates(list(settings.XGDS_MAP_SERVER_HANDLEBARS_DIRS), 'XGDS_MAP_SERVER_HANDLEBARS_DIRS')})
                              )            


@login_required 
def viewSampleByLabel(request, labelNum):
    try:
        label, create = LABEL_MODEL.get().objects.get_or_create(number=labelNum)
        if create:
            return editSample(request, label.sample.pk)
        else:
            return redirect(reverse('search_map_single_object', kwargs={'modelPK':label.sample.pk,
                                                                        'modelName': settings.XGDS_SAMPLE_SAMPLE_KEY}))   
    except:
        return createSample(request, labelNum)


def createSample(request, labelNum, label=None):
    """
    Create a label and/or sample based on the requested label number
    """
    if not label:
        label, create = LABEL_MODEL.get().objects.get_or_create(number=labelNum)
    sample, sample_create = SAMPLE_MODEL.get().objects.get_or_create(label=label)
    if sample_create:
        label.url = reverse('search_map_single_object', kwargs={'modelName':settings.XGDS_SAMPLE_SAMPLE_KEY,
                                                                'modelPK':sample.pk})
        label.save() 
    form = SampleForm(instance=sample)
    return editSample(request, sample.pk, form)


def setSampleCustomFields(form, sample):       
    # set custom field values with existing data.
    positionDict = sample.getPositionDict()
    form.fields['latitude'].initial = positionDict['lat']
    form.fields['longitude'].initial = positionDict['lon']
    if 'altitude' in positionDict:
        form.fields['altitude'].initial = positionDict['altitude']
    if sample.collection_time:
        form.fields['collection_time'].initial = sample.collection_time
    if sample.collector:
        form.fields['collector'].initial = sample.collector.first_name + ' ' + sample.collector.last_name
    return form


@login_required 
def getSampleEditPage(request):
    label = None
    if request.POST:
        numberOrName = request.POST['label_num_or_sample_name'] 
        if not numberOrName:
            messages.error(request, 'Please enter a valid sample name or label number')
            return render_to_response('xgds_sample/recordSample.html',
                                       RequestContext(request, {}))
        labelNum = None
        label = None
        sample = None 
        try:
            labelNum = int(numberOrName)
        except:
            try:
                sample = SAMPLE_MODEL.get().objects.get(name=numberOrName)
                label = sample.label
            except:
                messages.error(request, 'Could not find sample %s; start with a label. ' % numberOrName,
                               extra_tags='safe')
                return render_to_response('xgds_sample/recordSample.html',
                                          RequestContext(request, {}))
        
        if labelNum and not label:
            try:
                label = LABEL_MODEL.get().objects.get(number=labelNum)
                sample = label.sample
            except:
                return createSample(request, labelNum, label)
        form = SampleForm(instance=sample)
        return editSample(request, sample.pk, form)


@login_required 
def editSampleByLabel(request, labelNum):
    """ make changes to a sample based on form inputs and save,
    OR open the edit page
    """
    # get all user names (first last). Needed for autocompleting collector field.
    try:
        label, create = LABEL_MODEL.get().objects.get_or_create(number=labelNum)
        sample = label.sample
    except: 
        return createSample(request, labelNum, label)
    # if is updating the sample info from edit form
    if request.method == "POST":
        # swap the user id 
        form = SampleForm(request.POST, instance=sample)
        if form.is_valid():
            form.save()
            if form.errors:
                for key, msg in form.errors.items():
                    if key == 'warning':
                        messages.warning(request, msg)
                    elif key == 'error': 
                        messages.error(request, msg)
            else:
                messages.success(request, 'Sample data successfully updated.')
            return redirect(reverse('search_map_single_object', kwargs={'modelPK': form.instance.pk,
                                                                        'modelName': settings.XGDS_SAMPLE_SAMPLE_KEY})) 
#             return render_to_response('xgds_sample/sampleView.html',
#                                        RequestContext(request, {'sample': form.instance}))
        else: 
            messages.error(request, 'The form is not valid')
            return editSample(request, sample.pk, form)
            
    # edit page opened via edit/<label number>
    elif request.method == "GET":
        form = SampleForm(instance=sample)
        return editSample(request, sample.pk, form)
    
    
@login_required
def getSampleLabelsPage(request):
    labels = LABEL_MODEL.get().objects.all()
    return render_to_response('xgds_sample/sampleLabels.html',
                              RequestContext(request,
                                             {'labels': labels,
                                              'file_url': ""}))

def chunks(l, n):
    n = max(1, n)
    return [l[i:i + n] for i in range(0, len(l), n)]


def printSampleLabels(request):
    data = {'file_url': ""}
    if request.method == 'POST': 
        if 'label_quantity' in request.POST:
            quantity = int(request.POST['label_quantity'])
            labels = LABEL_MODEL.get().objects.all()
            data['labels'] = labels
            aggregate = labels.aggregate(Max('number'))
            if aggregate['number__max']:
                startNum = aggregate['number__max'] + 1
            else:
                startNum = 1
            labelNumbers = range(startNum, startNum + quantity)
            labelsToPrint = []
            for labelNum in labelNumbers:
                label, create = LABEL_MODEL.get().objects.get_or_create(number=int(labelNum))
                sample, sample_create = SAMPLE_MODEL.get().objects.get_or_create(label=label)
                sample.save()
                if sample_create:
                    label.url = reverse('search_map_single_object', kwargs={'modelName':settings.XGDS_SAMPLE_SAMPLE_KEY,
                                                                            'modelPK':sample.pk})
                    label.save() 
                labelsToPrint.append(label)
            if quantity <=0:
                messages.error(request, "Quantity must be an integer greater than 0.")
            else: 
                messages.error(request, "")
        else: 
            labelIds = request.POST.getlist('label_checkbox')
            labelsToPrint = [LABEL_MODEL.get().objects.get(id=int(labelId)) for labelId in labelIds]
        if labelsToPrint:
            size = SampleLabelSize.objects.get(name="small")
            labelChunks = chunks(labelsToPrint, 10)  # labels in chunks of 10. (list of lists)
            pdfFileNames = []
            index = 0
            for labelChunk in labelChunks: 
                pdfFileName = generateMultiPDF(labelChunk, size, index)
                pdfFileNames.append(pdfFileName)
                index = index + 1
            
            # merge the single sheet of pdf files into one to create multiple page pdf.
            merger = PdfFileMerger()
            outputFileName = re.sub(r"_temp\d+", "", pdfFileNames[0])
            for filename in pdfFileNames:
                merger.append(PdfFileReader(file(filename, 'rb')))
                # delete the temporary file
                os.remove(filename)
            merger.write(outputFileName)  # merge them into one file, and take the first file's name

            outputFileName = outputFileName.replace(settings.DATA_ROOT, settings.DATA_URL)
            messages.success(request, "Labels successfully generated.")
            data['file_url'] = outputFileName         
#             if pdfFileName:
#                 pdfFileName = pdfFileName.replace(settings.DATA_ROOT, settings.DATA_URL)
#                 messages.success(request, "Labels successfully generated.")
#                 data['file_url'] = pdfFileName
    return render_to_response('xgds_sample/sampleLabels.html', 
                               RequestContext(request, data))