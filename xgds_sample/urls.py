#__BEGIN_LICENSE__
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
#__END_LICENSE__

from django.conf.urls import url, include
from django.core.urlresolvers import reverse_lazy
from django.views.generic import RedirectView
from xgds_sample import views


urlpatterns = [url(r'labels$', views.getSampleLabelsPage, {}, 'xgds_sample_labels'),
               url(r'deleteLabel/(?P<labelNum>[\d]+)$', views.deleteLabelAndSample, {}, 'xgds_sample_delete_label'),
               url(r'edit/sample$', views.getSampleEditPage, {}, 'xgds_sample_record_edit'),
               url(r'edit/sample/(?P<samplePK>[\d]+)$', views.getSampleEditPage, {}, 'xgds_sample_record_edit'), 
               url(r'saveSample$', views.saveSampleInfo, {}, 'xgds_sample_info_save'),
               url(r'labels/print$', views.printSampleLabels, {}, 'xgds_sample_labels_print'),
               url(r'help$', views.getSampleHelpPage, {}, 'xgds_sample_help'),
               # url(r'^search/$', RedirectView.as_view(url=reverse_lazy('search_map_object', kwargs={'modelName':'Sample'}), permanent=False), name='xgds_sample_fullsearch'),
#               url(r'^search/$', RedirectView.as_view(url=reverse('search_map_object'), permanent=False), {'modelName':'Sample'},  'xgds_sample_fullsearch'),
               
               # Including these in this order ensures that reverse will return the non-rest urls for use in our server
               url(r'^rest/', include('xgds_sample.restUrls')),
               url('', include('xgds_sample.restUrls')),

               ]

