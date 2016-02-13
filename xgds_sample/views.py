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
from xgds_sample.models import SampleType, Region, Label
import logging

import json

SAMPLE_MODEL = LazyGetModelByName(settings.XGDS_SAMPLE_SAMPLE_MODEL)
LABEL_MODEL = LazyGetModelByName(settings.XGDS_SAMPLE_LABEL_MODEL)


@login_required
def getSampleCreatePage(request):
    return render_to_response('xgds_sample/sampleCreate.html', 
                              RequestContext(request, {}))
  
    
def createSample(request):
    if request.method == 'POST':
        try:
            labelNum = request.POST['labelNumber']
        except: 
            labelNum = None
        form = SampleForm()
        if labelNum:
            # create a sample from label
            try:
                sample = SAMPLE_MODEL.get().objects.get(label__number=labelNum)
            except:
                label = LABEL_MODEL.get().objects.get(number=labelNum)
                sample = SAMPLE_MODEL.get().objects.create(label=label)
        else:
            # update a sample from label.
            sample = SAMPLE_MODEL.get().objects.get(id=request.POST['sampleId'])
            if sample:
                form = SampleForm(request.POST, instance=sample)
                if form.is_valid():
                    form.save()
            else: 
                return HttpResponse('Sample should exist but it does not', status=400)
        return render_to_response('xgds_sample/sampleCreateForm.html', 
                                  RequestContext(request, {'sample': sample,
                                                           'form': form,
                                                           'types_list': SampleType.objects.all(),
                                                           'regions_list': Region.objects.all(),
                                                           'labels_list': Label.objects.all()
                                                           }))

def updateSample(sample):    
    try:
        name = request.POST['Name']
        sample.updateSampleFromName(name)
    except:
        sample.updateSampleFromForm(request.POST)


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
