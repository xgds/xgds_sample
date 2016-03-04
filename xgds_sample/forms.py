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
import datetime

from django.conf import settings
from django import forms
from django.forms import ModelForm
from geocamUtil.loader import getModelByName
from xgds_sample.models import SampleType, Region
from geocamUtil.loader import LazyGetModelByName

LOCATION_MODEL = LazyGetModelByName(settings.GEOCAM_TRACK_PAST_POSITION_MODEL)


class SampleForm(ModelForm):
    latitude = forms.CharField(required=False, label="Latitude:")
    longitude = forms.CharField(required=False, label="Longitude:")
    collection_time = forms.DateTimeField(required=False)
    
    class Meta: 
        model = getModelByName(settings.XGDS_SAMPLE_SAMPLE_MODEL)
        exclude = ['location', 
                   'name', 
                   'creation_time', 
                   'modification_time', 
                   'creator', 
                   'modifier', 
                   'label']
    
    def save(self, commit=True):
        instance = super(SampleForm, self).save(commit=False)
        if self.cleaned_data['collection_time']:
            instance.collection_time = self.cleaned_data['collection_time']
        if self.cleaned_data['latitude'] and self.cleaned_data['longitude']:
            if instance.location is None:
                instance.location = LOCATION_MODEL.get().objects.create(serverTimestamp = datetime.datetime.utcnow(),
                                                                        timestamp = datetime.datetime.now(),
                                                                        latitude = self.cleaned_data['latitude'],
                                                                        longitude = self.cleaned_data['longitude'])
            else:
                instance.location.latitude = self.cleaned_data['latitude']
                instance.location.longitude = self.cleaned_data['longitude']
                instance.location.timestamp = datetime.datetime.now()
        if instance.name is None:
            instance.name = instance.buildName()
          
        if commit:
            instance.save()
        return instance
    