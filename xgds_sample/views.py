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


def getSampleLookupPage(request):
    return render_to_response('xgds_sample/sampleCreate.html', 
                              RequestContext(request, {}))

@login_required 
def getSampleViewPage(request, labelNum):
    label = get_object_or_404(LABEL_MODEL.get(), number=labelNum)
    sample = get_object_or_404(SAMPLE_MODEL.get(), label = label)
    return render_to_response('xgds_sample/sampleView.html', 
                              RequestContext(request, {'sample': sample,
                                                       'labelNum': labelNum}))

@login_required 
def getSampleEditPage(request, labelNum):
    label = get_object_or_404(LABEL_MODEL.get(), number=labelNum)
    sample = get_object_or_404(SAMPLE_MODEL.get(), label = label)
    form = SampleForm(sample.toMapDict(), instance=sample)
    data = {'sample': sample,
            'form': form,
            'labelNum': labelNum}
    return render_to_response('xgds_sample/sampleEditForm.html',
                              RequestContext(request,data))
    

@login_required    
def addOrUpdateSample(request, labelNum=None):
    if request.method == 'POST':
        # post request from the sample add or update form (just label num) 
        if not labelNum: 
            labelNum = request.POST['labelNum']
            if not labelNum:
                messages.error(request,'Please enter a valid integer label number')
                return render_to_response('xgds_sample/sampleCreate.html',
                                          RequestContext(request,{}))
            label, labelCreated = LABEL_MODEL.get().objects.get_or_create(number = labelNum)
            sample, sampleCreated = SAMPLE_MODEL.get().objects.get_or_create(label = label)
            if sampleCreated:
                form = SampleForm()
                templateName = 'xgds_sample/sampleEditForm.html'
            else: 
                form = SampleForm(sample.toMapDict())
                templateName = 'xgds_sample/sampleView.html'
            return render_to_response(templateName,
                                     RequestContext(request, {'sample': sample,
                                                              'form': form,
                                                              'labelNum': labelNum}))
        # post request sent from sample edit form. 
        else: 
            sampleId = request.POST['sampleId']
            sample = SAMPLE_MODEL.get().objects.get(pk = sampleId)   
            if not sample:
                messages.error(request,'Invalid sample with id %d' % sampleId)
                data = {}
            else: 
                form = SampleForm(request.POST, instance=sample)
                if form.is_valid():
                    form.save()
                    messages.success(request, 'Sample data successfully updated.')
                    data = {'sample': sample,
                            'form': form,
                            'labelNum': labelNum}
                else: 
                    messages.error(request, 'invalid form')
                    data = {}
            return render_to_response('xgds_sample/sampleCreate.html',
                                      RequestContext(request,data))



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
