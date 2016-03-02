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
from xgds_sample.models import SampleType, Region
import logging
import json
from geocamUtil.datetimeJsonEncoder import DatetimeJsonEncoder


SAMPLE_MODEL = LazyGetModelByName(settings.XGDS_SAMPLE_SAMPLE_MODEL)
LABEL_MODEL = LazyGetModelByName(settings.XGDS_SAMPLE_LABEL_MODEL)

# view helper
def getSampleInfoFromLabelNum(labelNum):
    # render sample edit (view) page
    label, labelCreated = LABEL_MODEL.get().objects.get_or_create(number = labelNum)
    sample, sampleCreated = SAMPLE_MODEL.get().objects.get_or_create(label = label)
    if sampleCreated:
        form = SampleForm()
        editFlag = True
    else: # sample already existed in the database
        form = SampleForm(sample.toMapDict())
        editFlag = False
    data = {'sample': sample,
            'form': form,
            'labelNum': labelNum, 
            'editable': editFlag}
    return data


@login_required    
def addOrUpdateSample(request, labelNum=None):
    if request.method == 'GET':
        if labelNum: 
            data = getSampleInfoFromLabelNum(labelNum)
            return render_to_response('xgds_sample/sampleEditForm.html', 
                                      RequestContext(request, data))
        else: 
            # render the sample create form (just label number entry)
            return render_to_response('xgds_sample/sampleCreate.html', 
                                      RequestContext(request, {}))
    if request.method == 'POST':
        # Update sample data via the sample edit form
        if labelNum:
            sampleId = request.POST['sampleId']
            sample = SAMPLE_MODEL.get().objects.get(pk = sampleId)
            if sample: 
                form = SampleForm(request.POST, instance=sample)
                if form.is_valid():
                    form.save()
                    data = {'sample': sample,
                            'form': form,
                            'labelNum': labelNum}
                    messages.success(request, 'Sample data successfully updated.')
                else:
                    print "form is not valid"
                    print form.errors
                    messages.error(request, 'invalid form')
                    data = {}
            else: 
                print "sample does not exist"
                messages.error(request, 'Valid sample does not exist.')
                data = {}
        # Render sample edit form the sample create form
        else: 
            labelNum = request.POST['labelNumber']
            if not labelNum:
                messages.error(request,'Please enter a valid integer label number')
                return render_to_response('xgds_sample/sampleCreate.html',
                                          RequestContext(request,{}))
            data = getSampleInfoFromLabelNum(labelNum)
        return render_to_response('xgds_sample/sampleEditForm.html', 
                                  RequestContext(request, data))


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
