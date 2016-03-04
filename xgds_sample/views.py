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
from django.shortcuts import render_to_response, render, get_object_or_404
from django.core.urlresolvers import reverse
from django.http import (HttpResponseRedirect, 
                         HttpResponseForbidden, 
                         Http404, 
                         HttpResponse, 
                         HttpResponseNotAllowed)
from django.template import RequestContext
from django.utils.translation import ugettext, ugettext_lazy as _
from django.forms.formsets import formset_factory
from django.conf import settings
from django.contrib import messages 

from geocamUtil.loader import getClassByName, LazyGetModelByName
from forms import SampleForm
from xgds_data.forms import SearchForm, SpecializedForm
from xgds_sample.models import SampleType, Region
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
    samplesJson = [] #TODO
    data = {'formset': theFormSet,
            'samplesJsonArray': samplesJson}
    return render_to_response("xgds_sample/sampleSearch.html", data,
                              context_instance=RequestContext(request))

@login_required
def getRecordSamplePage(request):
    return render_to_response('xgds_sample/recordSample.html', 
                              RequestContext(request, {}))


def getSampleDictForSampleView(sample):
    # return the displayable dict.
    sampleDict = sample.toMapDict()
    sampleDict['region'] = sample.region.name
    sampleDict['type'] = sample.type.display_name
    sampleDict['label'] = sample.number
    sampleDict['triplicate'] = sample.triplicate.display_name
    return sampleDict 

    
@login_required 
def getSampleViewPage(request, labelNum):
    label = get_object_or_404(LABEL_MODEL.get(), number=labelNum)
    sample = get_object_or_404(SAMPLE_MODEL.get(), label = label)
    sampleDict = getSampleDictForSampleView(sample)

    return render_to_response('xgds_sample/sampleView.html', 
                              RequestContext(request, {'sampleDict': sampleDict,
                                                       'labelNum': labelNum}))

def createSample(request, labelNum=None):
    label = get_object_or_404(LABEL_MODEL.get(), number=labelNum) 
    sample = SAMPLE_MODEL.get().objects.create(label=label)
    return HttpResponseRedirect(reverse('xgds_sample_edit', kwargs={'labelNum': labelNum}))


def createSampleFromLabel(request, labelNum = None):
    label = LABEL_MODEL.get().objects.create(number = labelNum)
    sample, create = SAMPLE_MODEL.get().objects.get_or_create(label=label)
    return HttpResponseRedirect(reverse('xgds_sample_edit', kwargs={'labelNum': labelNum}))


@login_required 
def getSampleEditPage(request, labelNum=None):
    if labelNum: 
        label = get_object_or_404(LABEL_MODEL.get(), number=labelNum) 
        sample = get_object_or_404(SAMPLE_MODEL.get(), label = label)
        form = SampleForm(request.POST, instance=sample)
        # if is updating the sample info from edit form
        if request.POST: 
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
        elif request.GET:
            data = {'sample': sample,
                    'form': form,
                    'labelNum': labelNum}
            return render_to_response('xgds_sample/sampleEditForm.html',
                                      RequestContext(request,data))
    else: 
        numberOrName = request.POST['label_num_or_sample_name'] 
        sample = None
        form = None
        labelNum = None
        # handle empty user input. 
        if not numberOrName:
            messages.error(request, 'Please enter a valid sample name or label number')
            return render_to_response('xgds_sample/recordSample.html',
                                       RequestContext(request, {}))
        
        # if user entered sample name
        if numberOrName and numberOrName[0].isalpha():
            try: 
                sample = SAMPLE_MODEL.get().objects.get(name = numberOrName)
                labelNum = sample.label.number
            except: 
                # If no sample with the given sample name, show an error. 
                messages.error(request, 'No matching sample with given name %s. Please enter a label name first.' % numberOrName)
                return render_to_response('xgds_sample/recordSample.html',
                                           RequestContext(request, {}))
        # if user entered a label number
        else: 
            labelNum = numberOrName
            try: 
                label = LABEL_MODEL.get().objects.get(number=numberOrName)
            except: 
                messages.error(request, 'There is no matching sample. Would you like to create one?  <a href=createSampleFromLabel/' + labelNum + '>create</a>',
                               extra_tags='safe')
                return render_to_response('xgds_sample/recordSample.html',
                                          RequestContext(request, {}))
            else: 
                try: 
                    sample = SAMPLE_MODEL.get().objects.get(label = label)
                except: 
                    messages.error(request, 'There is no matching sample. Would you like to create one? <a href=createSample/' + labelNum + '>create</a>',
                                   extra_tags='safe')
                    return render_to_response('xgds_sample/recordSample.html',
                                              RequestContext(request, {}))
        form = SampleForm(sample.toMapDict(), instance=sample)
    data = {'sample': sample,
            'form': form,
            'labelNum': labelNum}
    return render_to_response('xgds_sample/sampleEditForm.html',
                              RequestContext(request,data))
    
    
@login_required
def getSampleLabelsPage(request):
    return render_to_response('xgds_sample/sampleLabels.html', 
                              RequestContext(request,{}))
