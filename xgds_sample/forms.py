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
import pytz

from django.conf import settings
from django import forms
from django.forms import ModelForm
from geocamUtil.loader import getModelByName
from xgds_sample.models import SampleType, Region
from geocamUtil.loader import LazyGetModelByName
from geocamTrack.views import getClosestPosition

LOCATION_MODEL = LazyGetModelByName(settings.GEOCAM_TRACK_PAST_POSITION_MODEL)


class SampleForm(ModelForm):
    latitude = forms.FloatField(required=False, label="Latitude:")
    longitude = forms.FloatField(required=False, label="Longitude:")
    altitude = forms.FloatField(required=False, label="Altitude:")
    date_formats = list(forms.DateTimeField.input_formats) + [
        '%Y/%m/%d %H:%M:%S',
        '%Y-%m-%d %H:%M:%S',
        '%m/%d/%Y %H:%M'
    ]
    collection_time = forms.DateTimeField(required=False, input_formats=date_formats)
    collection_timezone = forms.CharField(widget=forms.HiddenInput(), initial=settings.TIME_ZONE)
    
    class Meta: 
        model = getModelByName(settings.XGDS_SAMPLE_SAMPLE_MODEL)
        exclude = ['track_position', 
                   'user_position', 
                   'name', 
                   'creation_time', 
                   'modification_time', 
                   'creator', 
                   'modifier', 
                   'label']
    
    # populate the event time with NOW if it is blank.
    def clean_collection_time(self):
        ctime = self.cleaned_data['collection_time']
        
        if not ctime:
            return None
        else:
            ctimezone = self.cleaned_data['collection_timezone']
            tz = pytz.timezone(ctimezone)
            localizedTime = tz.localize(ctime)
            return localizedTime.astimezone(pytz.utc)
    
    def save(self, commit=True):
        instance = super(SampleForm, self).save(commit=False)
        if instance.resource and instance.collection_time:
            instance.track_position = getClosestPosition(timestamp=instance.collection_time, resource=instance.resource)

        if self.cleaned_data['latitude'] and self.cleaned_data['longitude']:
            if instance.location is None:
                instance.user_position = LOCATION_MODEL.get().objects.create(serverTimestamp = datetime.datetime.now(pytz.utc),
                                                                             timestamp = datetime.datetime.now(pytz.utc),
                                                                             latitude = self.cleaned_data['latitude'],
                                                                             longitude = self.cleaned_data['longitude'])
                if self.cleaned_data['altitude']:
                    instance.user_position.altitude = self.cleaned_data['altitude'] 
            else:
                instance.user_position.latitude = self.cleaned_data['latitude']
                instance.user_position.longitude = self.cleaned_data['longitude']
                if self.cleaned_data['altitude']:
                    instance.user_position.altitude = self.cleaned_data['altitude'] 
        if instance.name is None:
            instance.name = instance.buildName()
          
        if commit:
            instance.save()
        return instance
    