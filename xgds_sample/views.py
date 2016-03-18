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

from datetime import datetime, timedelta
import pytz

from django.contrib.auth.decorators import login_required
from django.shortcuts import render_to_response, render, get_object_or_404
from django.core.urlresolvers import reverse
from django.http import (HttpResponseRedirect,
                         HttpResponseForbidden,
                         HttpResponseBadRequest,
                         Http404,
                         HttpResponse,
                         HttpResponseNotAllowed)
from django.template import RequestContext
from django.utils.translation import ugettext, ugettext_lazy as _
from django.forms.formsets import formset_factory
from django.conf import settings
from django.contrib import messages 
from django.views.decorators.cache import never_cache


from geocamUtil.loader import getClassByName, LazyGetModelByName
from forms import SampleForm
from xgds_data.forms import SearchForm, SpecializedForm
from xgds_sample.models import SampleType, Region
from xgds_map_server.views import get_handlebars_templates
import logging
import json
from geocamUtil.datetimeJsonEncoder import DatetimeJsonEncoder


SAMPLE_MODEL = LazyGetModelByName(settings.XGDS_SAMPLE_SAMPLE_MODEL)
LABEL_MODEL = LazyGetModelByName(settings.XGDS_SAMPLE_LABEL_MODEL)


@login_required
def getSampleSearchPage(request):
    theForm = SpecializedForm(SearchForm, SAMPLE_MODEL.get())
    theFormSetMaker = formset_factory(theForm, extra=0)
    theFormSet = theFormSetMaker(initial=[{'modelClass': SAMPLE_MODEL.get()}])
    samplesJson = []  # TODO
    fullTemplateList = list(settings.XGDS_MAP_SERVER_HANDLEBARS_DIRS)
    fullTemplateList.append(settings.XGDS_SAMPLE_HANDLEBARS_DIR[0])
    data = {'formset': theFormSet,
            'samplesJsonArray': samplesJson,
            'templates': get_handlebars_templates(fullTemplateList)
            }
    return render_to_response("xgds_sample/sampleSearch.html", data,
                              context_instance=RequestContext(request))


@login_required 
def getSampleViewPage(request, labelNum):
    label = get_object_or_404(LABEL_MODEL.get(), number=labelNum)
    try:
        sample = label.sample
        data = {'sample': sample} 
        return render_to_response('xgds_sample/sampleView.html',
                              RequestContext(request, data))
    except: 
        messages.error(request, 'There is no matching sample. Would you like to create one?  <a href=createSample/' + str(labelNum) + '>create</a>',
                       extra_tags='safe')
        return render_to_response('xgds_sample/recordSample.html',
                                  RequestContext(request, {}))
        

def createSample(request, labelNum=None):
    """
    Create a label and/or sample based on the requested label number
    """
    label, create = LABEL_MODEL.get().objects.get_or_create(number=labelNum)
    sample, create = SAMPLE_MODEL.get().objects.get_or_create(label=label)
    form = SampleForm(instance=sample)
    data = {'form': form}
    return render_to_response('xgds_sample/sampleEditForm.html',
                              RequestContext(request, data))


@login_required
def getRecordSamplePage(request):
    return render_to_response('xgds_sample/recordSample.html',
                              RequestContext(request, {}))
    
    
def setSampleCustomFields(form, sample):       
    # set custom field values with existing data.
    positionDict = sample.getPositionDict()
    form.fields['latitude'].initial = positionDict['lat']
    form.fields['longitude'].initial = positionDict['lon']
    if 'altitude' in positionDict:
        form.fields['altitude'].initial = positionDict['altitude']
        
    if sample.collection_time:
        form.fields['collection_time'].initial = sample.collection_time
    return form


@login_required 
def getSampleEditPage(request):
    if request.POST:
        numberOrName = request.POST['label_num_or_sample_name'] 
        if not numberOrName:
            messages.error(request, 'Please enter a valid sample name or label number')
            return render_to_response('xgds_sample/recordSample.html',
                                       RequestContext(request, {}))
        # if user entered sample name
        if numberOrName and numberOrName[0].isalpha():
            try: 
                sample = SAMPLE_MODEL.get().objects.get(name=numberOrName)
                labelNum = sample.label.number
            except: 
                # If no sample with the given sample name, show an error. 
                messages.error(request, 'No matching sample with given name %s. Please enter a label name first.' % numberOrName)
                return render_to_response('xgds_sample/recordSample.html',
                                           RequestContext(request, {}))
        else: # expecting a number
            try: 
                labelNum = int(numberOrName)
            except:
                messages.error(request, 'Invalid entry; label number must be a number or enter sample name.',
                               extra_tags='safe')
                return render_to_response('xgds_sample/recordSample.html',
                                          RequestContext(request, {}))
            try:
                label = LABEL_MODEL.get().objects.get(number=labelNum)
            except: 
                messages.error(request, 'There is no matching sample. Would you like to create one?  <a href=createSample/' + str(labelNum) + '>create</a>',
                               extra_tags='safe')
                return render_to_response('xgds_sample/recordSample.html',
                                          RequestContext(request, {}))
            try: 
                sample = SAMPLE_MODEL.get().objects.get(label=label)
            except: 
                messages.error(request, 'There is no matching sample. Would you like to create one? <a href=createSample/' + str(labelNum) + '>create</a>',
                               extra_tags='safe')
                return render_to_response('xgds_sample/recordSample.html',
                                          RequestContext(request, {})) 
        form = SampleForm(instance=sample)
        # set custom field values with existing data.
        form = setSampleCustomFields(form, sample)
        data = {'form': form} 
        return render_to_response('xgds_sample/sampleEditForm.html',
                                  RequestContext(request, data))
    else: 
        return HttpResponseBadRequest("Request.%s not allowed" % request.method)


@login_required 
def updateSampleRecord(request, labelNum):
    """ make changes to a sample based on form inputs and save,
    OR open the edit page
    """
    label = get_object_or_404(LABEL_MODEL.get(), number=labelNum) 
    try: 
        sample = label.sample
    except: 
        messages.error(request, 'There is no matching sample. Would you like to create one?  <a href=createSample/' + str(labelNum) + '>create</a>',extra_tags='safe')
        return render_to_response('xgds_sample/recordSample.html',
                                  RequestContext(request, {}))
    # if is updating the sample info from edit form
    if request.method == "POST":
        form = SampleForm(request.POST, instance=sample)
        if form.is_valid():
            form.save()
            messages.success(request, 'Sample data successfully updated.')
            return render_to_response('xgds_sample/recordSample.html',
                                       RequestContext(request, {}))
        else: 
            messages.error(request, 'The form is not valid')
            return render_to_response('xgds_sample/sampleEditForm.html',
                                      RequestContext(request, {'sample': sample,
                                                               'form': form,
                                                               'labelNum': labelNum}))
    # edit page opened via edit/<label number>
    elif request.method == "GET":
        form = SampleForm(instance=sample) 
        form = setSampleCustomFields(form, sample)
        data = {'form': form}
        return render_to_response('xgds_sample/sampleEditForm.html',
                                  RequestContext(request, data))
    else: 
        return HttpResponseBadRequest("Request type %s is invalid." % request.method)
    
    
@login_required
def getSampleLabelsPage(request):
    labels = LABEL_MODEL.get().objects.all()
    labelsJson = [json.dumps(label.toMapDict()) for label in labels] 
    # add sample name and printed date to the array.
    return render_to_response('xgds_sample/sampleLabels.html',
                              RequestContext(request,
                                             {'labelsJson': labelsJson,
                                              'STATIC_URL': settings.STATIC_URL, #TODO you don't need to do this, you can access all settings in the template ie {{ STATIC_URL }}
                                              'createLabelUrl': reverse('xgds_sample_labels_create')}))
    
    
def createSampleLabels(request):
    if request.POST:
        try: 
            startNum = int(request.POST['start_number'])
        except: 
            return HttpResponse(json.dumps({'status': 'error', 'message': 'Invalid argument. Please enter an integer.'}), 
                         content_type = 'application/json')
        try: 
            quantity = int(request.POST['quantity'])
        except: 
            return HttpResponse(json.dumps({'status': 'error', 'message': 'Invalid argument. Please enter an integer.'}), 
                         content_type = 'application/json')
        # create multiple labels
        newLabels = []
        for labelNum in range(startNum, startNum + quantity):
            label, created = LABEL_MODEL.get().objects.get_or_create(number = labelNum)
            if created:
                newLabels.append(json.dumps(label.toMapDict()))
        if newLabels:
            return HttpResponse(json.dumps({'status': 'success', 
                                            'message': 'Successfully created the labels',
                                            'newLabels': newLabels}), 
                                    content_type='application/json')
        else: 
            return HttpResponse(json.dumps({'status': '', 
                                'message': 'No new labels to create.',
                                'newLabels': newLabels}), 
                                content_type='application/json') 

