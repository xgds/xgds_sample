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

from django.shortcuts import render_to_response
from django.http import HttpResponseRedirect, HttpResponseForbidden, Http404
from django.template import RequestContext
from django.utils.translation import ugettext, ugettext_lazy as _
from django.forms.formsets import formset_factory
from django.conf import settings
from geocamUtil.loader import LazyGetModelByName

from forms import SampleForm
from xgds_data.forms import SearchForm, SpecializedForm
from geocamUtil.loader import getClassByName


SAMPLE_MODEL = LazyGetModelByName(settings.XGDS_SAMPLE_SAMPLE_MODEL)


def getSampleImportPage(request):
    data = {'form': SampleForm()}
    return render_to_response("xgds_sample/sampleImport.html", data, 
                              context_instance=RequestContext(request))


def getSampleSearchPage(request):
    theForm = SpecializedForm(SearchForm, SAMPLE_MODEL.get())
    theFormSetMaker = formset_factory(theForm, extra=0)
    theFormSet = theFormSetMaker(initial=[{'modelClass': SAMPLE_MODEL.get()}])
    data = {'formset': theFormSet}
    return render_to_response("xgds_sample/sampleSearch.html", data,
                              context_instance=RequestContext(request))
