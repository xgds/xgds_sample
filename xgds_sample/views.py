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
from django.shortcuts import render_to_response, render
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

import json

SAMPLE_MODEL = LazyGetModelByName(settings.XGDS_SAMPLE_SAMPLE_MODEL)


def updateSampleDataFromName(sample, name):
    pass


def generateSampleName(sample):
    pass
#[2-char Region ID]    [2-digit year]    [1-char sample type]    [hyphen]    [3-digit number]    [1-char triplicates]


@login_required
def createNewSample(request):
    if request.method == 'GET':
        form = SampleForm()
        messages.success(request, '')
    elif request.method == 'POST':
        form = SampleForm(request.POST)
        if form.is_valid():
            new_sample = form.save()
            try:
                name = request.POST['Name']
                new_sample = updateSampleDataFromName(new_sample, name)
            except:
                name = None
                name = generateSampleName(new_sample)
                new_sample.name = name
            new_sample.save()
            # if there is no name, construct one.
            # if there is name, get the info from the name.
            
            print "request.POST in new sample"
            print request.POST
            form.save()
            messages.success(request, 'Successful form save.') 
            return HttpResponseRedirect(reverse('create_new_sample'))
        else: 
            messages.error(request, 'Error in saving form. ')
    else: 
        return HttpResponseNotAllowed(['GET', 'POST'])        
    return render_to_response('xgds_sample/sampleCreate.html', 
                              RequestContext(request, {'form': form}))


def getSampleCreatePage(request):
    recentSamples = SAMPLE_MODEL.get().objects.all().order_by('-collection_time')
    recentSamplesJson = [json.dumps(sample.toMapDict()) for sample in recentSamples]
    data = {'form': SampleForm(), 
            'samplesJsonArray': recentSamplesJson}
    return render_to_response("xgds_sample/sampleCreate.html", data, 
                              context_instance=RequestContext(request))


def getSampleSearchPage(request):
    theForm = SpecializedForm(SearchForm, SAMPLE_MODEL.get())
    theFormSetMaker = formset_factory(theForm, extra=0)
    theFormSet = theFormSetMaker(initial=[{'modelClass': SAMPLE_MODEL.get()}])
    samplesJson = [] #TODO
    data = {'formset': theFormSet,
            'samplesJsonArray': samplesJson}
    return render_to_response("xgds_sample/sampleSearch.html", data,
                              context_instance=RequestContext(request))
