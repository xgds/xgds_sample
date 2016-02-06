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


@login_required
def createNewSample(request):
    if request.method == 'GET':
        form = SampleForm()
    elif request.method == 'POST':
        form = SampleForm(request.POST)
        if form.is_valid():
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
    data = {'form': SampleForm(), 
            }
    return render_to_response("xgds_sample/sampleCreate.html", data, 
                              context_instance=RequestContext(request))


def getSampleSearchPage(request):
    theForm = SpecializedForm(SearchForm, SAMPLE_MODEL.get())
    theFormSetMaker = formset_factory(theForm, extra=0)
    theFormSet = theFormSetMaker(initial=[{'modelClass': SAMPLE_MODEL.get()}])
    data = {'formset': theFormSet}
    return render_to_response("xgds_sample/sampleSearch.html", data,
                              context_instance=RequestContext(request))
