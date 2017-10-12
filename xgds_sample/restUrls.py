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
from django.conf.urls import url
from xgds_sample import views


urlpatterns = [url(r'sample.json', views.getSampleInfo, {}, 'xgds_sample_get_info'),
               ]

if settings.XGDS_NOTES_ENABLE_GEOCAM_TRACK_MAPPING:
    urlpatterns += [url(r'samples.kml', views.sample_map_kml, {'readOnly': True, 'securityTags': ['readOnly']}, 'sample_map_kml')]
    urlpatterns += [url(r'samplesFeed.kml', views.getKmlNetworkLink, {'readOnly': True, 'securityTags': ['readOnly']}, 'sample_map_kml_feed')]
