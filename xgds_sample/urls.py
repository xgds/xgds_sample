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
               url(r'label/sample/(?P<labelNum>[\d]+)$', views.viewSampleByLabel, {}, 'xgds_sample_search_view'),
               url(r'createSample/(?P<labelNum>[\d]+)$', views.createSample, {}, 'xgds_sample_create'),
               url(r'deleteLabel/(?P<labelNum>[\d]+)$', views.deleteLabelAndSample, {}, 'xgds_sample_delete_label'),
               url(r'recordSample', TemplateView.as_view(template_name='xgds_sample/recordSample.html'), {}, 'xgds_sample_record'),
               url(r'edit$', views.getSampleEditPage, {}, 'xgds_sample_record_edit'),
               url(r'edit/(?P<labelNum>[\d]+)$', views.editSampleByLabel, {}, 'xgds_sample_record_update'), 
               url(r'edit/sample/(?P<samplePK>[\d]+)$', views.editSample, {}, 'xgds_sample_edit_sample'), 
               url(r'labels/print$', views.printSampleLabels, {}, 'xgds_sample_labels_print')
               ]