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

from django.conf import settings
from django.conf.urls import patterns, include, url

from django.views.generic.base import TemplateView
from xgds_sample import views


urlpatterns = [url(r'labels$', views.getSampleLabelsPage, {}, 'xgds_sample_labels'),
               url(r'deleteLabel/(?P<labelNum>[\d]+)$', views.deleteLabelAndSample, {}, 'xgds_sample_delete_label'),
               url(r'edit/sample$', views.getSampleEditPage, {}, 'xgds_sample_record_edit'),
               url(r'edit/sample/(?P<samplePK>[\d]+)$', views.getSampleEditPage, {}, 'xgds_sample_record_edit'), 
               url(r'saveSample$', views.saveSampleInfo, {}, 'xgds_sample_info_save'),
               url(r'sample.json', views.getSampleInfo, {}, 'xgds_sample_get_info'),
               url(r'labels/print$', views.printSampleLabels, {}, 'xgds_sample_labels_print'),
               url(r'help$', views.getSampleHelpPage, {}, 'xgds_sample_help')
               ]