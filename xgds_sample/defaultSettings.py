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

import os
from geocamUtil.SettingsUtil import getOrCreateDict

XGDS_SAMPLE_SAMPLE_MODEL = 'xgds_sample.Sample'
XGDS_SAMPLE_LABEL_MODEL = 'xgds_sample.Label'
XGDS_SAMPLE_PERM_LINK_PREFIX = 'TODO:FIXME'

XGDS_SAMPLE_DEFAULT_COLLECTOR = 'EV2'
XGDS_SAMPLE_PDF_DIR = "xgds_sample/labels"
XGDS_CORE_TEMPLATE_DIRS = getOrCreateDict('XGDS_CORE_TEMPLATE_DIRS')
XGDS_CORE_TEMPLATE_DIRS[XGDS_SAMPLE_SAMPLE_MODEL] = [os.path.join('xgds_sample', 'templates', 'handlebars')]

XGDS_SAMPLE_HANDLEBARS_DIR = [os.path.join('xgds_sample', 'templates', 'handlebars')]

XGDS_MAP_SERVER_JS_MAP = getOrCreateDict('XGDS_MAP_SERVER_JS_MAP')
XGDS_SAMPLE_SAMPLE_KEY = 'Sample'
XGDS_SAMPLE_SAMPLE_MONIKER = 'Sample'

XGDS_MAP_SERVER_JS_MAP[XGDS_SAMPLE_SAMPLE_KEY] = {'ol': 'xgds_sample/js/olSampleMap.js',
                                                  'model': XGDS_SAMPLE_SAMPLE_MODEL,
                                                  'searchableColumns': ['name', 'description', 'flight_name', 'sample_type', 'extras'],
                                                  'columns': ['checkbox', 'collection_time', 'collection_timezone', 'name', 'sample_type_name', 'label_number', 'collector_name', 'vehicle_name', 'thumbnail_image_url', 'place_name', 'pk', 'lat', 'lon', 'alt', 'flight_name', 'app_label', 'model_type', 'type', 'description', 'extras', 'DT_RowId'],
                                                  'hiddenColumns': ['thumbnail_image_url', 'place_name', 'pk','lat', 'lon', 'alt', 'flight_name', 'vehicle_name', 'app_label', 'model_type', 'type', 'description', 'extras', 'DT_RowId'],
                                                  'columnTitles': ['Time', 'TZ', 'Name', 'Type', 'Label', 'Collector'],
                                                  'order_columns': ['pk', 'collection_time', 'collection_timezone', 'name',
                                                                    'sample_type__display_name', 'label__number', 'collector__first_name'],
                                                  'viewHandlebars': 'xgds_sample/templates/handlebars/sample-view.handlebars',
                                                  'event_time_field': 'collection_time',
                                                  'event_timezone_field': 'collection_timezone',
                                                  'search_form_class': 'xgds_sample.forms.SearchSampleForm',
                                                  }


XGDS_MAP_SERVER_JS_MAP['Label'] = {'model': XGDS_SAMPLE_LABEL_MODEL,
                                   'columns': ['number', 'url', 'last_printed', 'sampleName', 'pk'],
                                   } 

XGDS_DATA_MASKED_FIELDS = getOrCreateDict('XGDS_DATA_MASKED_FIELDS')
XGDS_DATA_MASKED_FIELDS['xgds_sample'] = {'AbstractSample': ['track_position',
                                                             'user_position', 
                                                             'creator',
                                                             'modifier',
                                                             'creation_time',
                                                             'modification_time', 
                                                          ],
                                        }

XGDS_DATA_EXPAND_RELATED = getOrCreateDict('XGDS_DATA_EXPAND_RELATED')
XGDS_DATA_EXPAND_RELATED['xgds_sample'] = {'AbstractSample': [('place', 'site', 'Site')]}

XGDS_SAMPLES_SAMPLE_CHANNEL = 'Sample'
