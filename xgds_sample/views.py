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
from django.utils import timezone
from django.contrib.auth.models import User
from PyPDF2 import PdfFileMerger, PdfFileReader

from datetime import datetime
import json
import os
import re
import pytz

from geocamUtil.loader import getClassByName, LazyGetModelByName
from forms import SampleForm
from xgds_data.forms import SearchForm, SpecializedForm
from xgds_sample.models import SampleLabelSize, Region
from xgds_core.views import get_handlebars_templates
from geocamTrack.utils import getClosestPosition
from geocamUtil.models import SiteFrame
from geocamUtil.TimeUtil import utcToLocalTime

from geocamUtil.datetimeJsonEncoder import DatetimeJsonEncoder
from django.views.static import serve
from xgds_sample.labels import *

from django.http import HttpResponse
from StringIO import StringIO


SAMPLE_MODEL = LazyGetModelByName(settings.XGDS_SAMPLE_SAMPLE_MODEL)
LABEL_MODEL = LazyGetModelByName(settings.XGDS_SAMPLE_LABEL_MODEL)

TRACK_MODEL = LazyGetModelByName(settings.GEOCAM_TRACK_TRACK_MODEL)
POSITION_MODEL = LazyGetModelByName(settings.GEOCAM_TRACK_PAST_POSITION_MODEL)
RESOURCE_MODEL = LazyGetModelByName(settings.GEOCAM_TRACK_RESOURCE_MODEL)

XGDS_SAMPLE_TEMPLATE_LIST = list(settings.XGDS_MAP_SERVER_HANDLEBARS_DIRS)
XGDS_SAMPLE_TEMPLATE_LIST = XGDS_SAMPLE_TEMPLATE_LIST + settings.XGDS_CORE_TEMPLATE_DIRS[settings.XGDS_SAMPLE_SAMPLE_MODEL]
    
# get all user names (string)
def getUserNames():
    allUsers = [user.first_name + ' ' + user.last_name  for user in User.objects.all()]
    allUsers = [str(x) for x in allUsers if x.strip()]
    return allUsers


def getTrackPosition(timestamp, resource):
    '''
    Look up and return the closest tracked position if there is one.
    '''
    return getClosestPosition(timestamp=timestamp, resource=resource)


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


def setSampleCustomFields(form, sample):       
    # set custom field values with existing data.
    positionDict = sample.getPositionDict()
    form.fields['latitude'].initial = positionDict['latitude']
    form.fields['longitude'].initial = positionDict['longitude']
    if 'altitude' in positionDict:
        form.fields['altitude'].initial = positionDict['altitude']
    if sample.collection_time:
        form.fields['collection_time'].initial = sample.collection_time
    if sample.collector:
        form.fields['collector'].initial = sample.collector.first_name + ' ' + sample.collector.last_name
    return form


@login_required 
def getSampleEditPage(request, samplePK = None):
    fieldsEnabledFlag = 0  # initially, sample info fields are disabled until user presses enter to submit label number or name
    getSampleInfoUrl = reverse('xgds_sample_get_info')
    currentLabelNum = ""
    if samplePK:
        sample = SAMPLE_MODEL.get().objects.get(pk=samplePK)
        currentLabelNum = sample.label.number
        fieldsEnabledFlag = 1  # if we get to this page from sample view, enable the fields.
    form = SampleForm()
    return render_to_response('xgds_sample/sampleEdit.html',
                              RequestContext(request, {'form': form,
                                                       'currentLabelNum': currentLabelNum,
                                                       'users': getUserNames(),
                                                       'modelName': settings.XGDS_SAMPLE_SAMPLE_KEY,
                                                       'templates': get_handlebars_templates(list(settings.XGDS_MAP_SERVER_HANDLEBARS_DIRS), 'XGDS_MAP_SERVER_HANDLEBARS_DIRS'),
                                                       'getSampleInfoUrl': getSampleInfoUrl,
                                                       'fieldsEnabledFlag': fieldsEnabledFlag})
                              )      
 
 
@login_required
def saveSampleInfo(request):
    getSampleInfoUrl = reverse('xgds_sample_get_info')
    if request.method == "POST":
        data = request.POST.dict()
        labelNum = int(data['hidden_labelNum'])
        name = data['hidden_name']
        
        if labelNum: 
            label, labelCreate = LABEL_MODEL.get().objects.get_or_create(number = labelNum)
            sample, sampleCreate = SAMPLE_MODEL.get().objects.get_or_create(label = label)
        elif name: 
            sample, sampleCreate = SAMPLE_MODEL.get().objects.get_or_create(name = name)
        else: 
            return render_to_response('xgds_sample/sampleEdit.html',
                              RequestContext(request, {'form': SampleForm(),
                                                       'users': getUserNames(),
                                                       'modelName': settings.XGDS_SAMPLE_SAMPLE_KEY,
                                                       'templates': get_handlebars_templates(list(settings.XGDS_MAP_SERVER_HANDLEBARS_DIRS), 'XGDS_MAP_SERVER_HANDLEBARS_DIRS'),
                                                       'getSampleInfoUrl': getSampleInfoUrl,
                                                       'fieldsEnabledFlag': 0})
                              )        

        # swap the user id 
        form = SampleForm(request.POST, instance=sample)
        fieldsEnabledFlag = 1  #enable fields so user can fix the form errors
        if form.is_valid():
            form.save()
            if form.errors:
                for key, msg in form.errors.items():
                    if key == 'warning':
                        messages.warning(request, msg)
                    elif key == 'error':
                        print "THERE IS A FORM ERROR!" 
                        messages.error(request, msg)
            else:
                messages.success(request, 'Sample data successfully updated.')  
                # form save was successful so go to a blank page for another sample info input
                form = SampleForm()
                fieldsEnabledFlag = 0  # initially, sample info fields are disabled until user presses enter to submit label number or name
        
        return render_to_response('xgds_sample/sampleEdit.html',
                          RequestContext(request, {'form': form,
                                                   'users': getUserNames(),
                                                   'modelName': settings.XGDS_SAMPLE_SAMPLE_KEY,
                                                   'templates': get_handlebars_templates(list(settings.XGDS_MAP_SERVER_HANDLEBARS_DIRS), 'XGDS_MAP_SERVER_HANDLEBARS_DIRS'),
                                                   'getSampleInfoUrl': getSampleInfoUrl,
                                                   'fieldsEnabledFlag': fieldsEnabledFlag})
                          )      
     
 
def getSampleInfo(request):
    """
    When user enters the label number of sample name
    this sends back the corresponding sample information
    to populate the sample edit form
    """
    if request.method == "POST":
        json_data = {}
        postDict = request.POST.dict()
        # get the sample either by name or label number
        if 'sampleName' in postDict:
            sampleName = postDict['sampleName']
            if sampleName:  # sampleName is not necessarily unique.
                try: 
                    sample = SAMPLE_MODEL.get().objects.filter(name=sampleName)[0]
                except: 
                    sample = SAMPLE_MODEL.get().objects.create(name=sampleName)
            else:
                raise Exception("Sample %s is not found." % sampleName)
        if 'labelNum' in postDict:
            labelNum = int(postDict['labelNum'])
            if labelNum:
                label, labelCreate = LABEL_MODEL.get().objects.get_or_create(number=labelNum)
                if label:
                    # create the sample
                    sample, sample_create = SAMPLE_MODEL.get().objects.get_or_create(label=label)
                else: 
                    raise Exception("Label with number %d is not found", labelNum)
        # get sample info as json to pass back to client side
        mapDict = sample.toMapDict()
        # set the default information (mirroring forms.py as initial values)
        if not mapDict['region']: 
            siteFrame = SiteFrame.objects.get(pk = settings.XGDS_CURRENT_SITEFRAME_ID)
            mapDict['region'] =  Region.objects.get(zone = siteFrame).id
        if not mapDict['number']:
            mapDict['number'] = sample.getCurrentNumber()
        # change the server time (UTC) to local time for display
        if not mapDict['collection_time']: 
            utc_time = timezone.now() 
        else: 
            # convert to a datetime object
            utc_time = mapDict['collection_time']
            utc_time = datetime.strptime(utc_time, '%m/%d/%Y %H:%M:%S') 
        local_time = utcToLocalTime(utc_time) 
        collection_time = local_time.strftime("%m/%d/%Y %H:%M:%S")
        mapDict['collection_time'] = collection_time
        try: 
            json_data = json.dumps([mapDict], indent=4)
        except: 
            return HttpResponseBadRequest('sample info is not in proper JSON format')
        return HttpResponse(json_data, content_type='application/json',
                            status=200)
    else: 
        raise Exception("Request method %s not supported." % request.method)
    
    
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
                    label.url = settings.XGDS_SAMPLE_PERM_LINK_PREFIX + reverse('search_map_single_object', kwargs={'modelName':settings.XGDS_SAMPLE_SAMPLE_KEY,
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
    return render_to_response('xgds_sample/sampleLabels.html', 
                               RequestContext(request, data))
    

def getSampleHelpPage(request):
    image1Url = settings.STATIC_URL + 'xgds_sample/images/Slide1.png'
    image2Url = settings.STATIC_URL + 'xgds_sample/images/Slide2.png'
    image3Url = settings.STATIC_URL + 'xgds_sample/images//Slide3.png'
    data = {'image1': image1Url,
            'image2': image2Url, 
            'image3': image3Url}
    return render_to_response('xgds_sample/sampleHelp.html', 
                              RequestContext(request, data))
    