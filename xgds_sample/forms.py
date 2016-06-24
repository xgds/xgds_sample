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

from django.utils import timezone
from django.conf import settings
from django import forms
from django.forms import ModelForm, CharField
from django.core.exceptions import ValidationError
from django.contrib.auth.models import User

from geocamUtil.loader import getModelByName
from xgds_sample.models import SampleType, Region, Label
from geocamUtil.loader import LazyGetModelByName
from geocamTrack.utils import getClosestPosition
from geocamUtil.models import SiteFrame
from geocamUtil.TimeUtil import utcToLocalTime


LOCATION_MODEL = LazyGetModelByName(settings.GEOCAM_TRACK_PAST_POSITION_MODEL)
SAMPLE_MODEL = LazyGetModelByName(settings.XGDS_SAMPLE_SAMPLE_MODEL)
GEOCAM_TRACK_RESOURCE_MODEL = LazyGetModelByName(settings.GEOCAM_TRACK_RESOURCE_MODEL)


class CollectorCharField(CharField):
    def label_from_instance(self, obj):
        return "TEST LABEL"


class SampleForm(ModelForm):
    latitude = forms.FloatField(required=False, label="Latitude")
    longitude = forms.FloatField(required=False, label="Longitude")
    altitude = forms.FloatField(required=False, label="Altitude")
    description = forms.CharField(widget=forms.Textarea, required=False, label="Description")
    number = forms.IntegerField(required=False, min_value=0, label="Number")
    station_number = forms.IntegerField(required=False, min_value=0, label="Station #")
    collector = forms.CharField(required=False, label="Collector")
    name = forms.CharField(required=False, label="Name", help_text='Name autofills on save.')
    
    hidden_labelNum = forms.IntegerField(widget = forms.HiddenInput(), required = False)
    hidden_name = forms.CharField(widget = forms.HiddenInput(), required = False)
    
    date_formats = list(forms.DateTimeField.input_formats) + [
        '%Y/%m/%d %H:%M:%S',
        '%Y-%m-%d %H:%M:%S',
        '%m/%d/%Y %H:%M'
    ]
    collection_time = forms.DateTimeField(required=True, input_formats=date_formats, help_text="")
    collection_timezone = forms.CharField(widget=forms.HiddenInput(), initial=settings.TIME_ZONE)
    
    field_order = SAMPLE_MODEL.get().getFieldOrder()
    
    def __init__(self, *args, **kwargs):
        super(SampleForm, self).__init__(*args, **kwargs)
        if self.instance:
            if self.instance.collector:
                self.fields['collector'].initial = self.instance.collector.first_name + ' ' + self.instance.collector.last_name
            positionDict = self.instance.getPositionDict()
            self.fields['latitude'].initial = positionDict['latitude']
            self.fields['longitude'].initial = positionDict['longitude']
            if 'altitude' in positionDict:
                self.fields['altitude'].initial = positionDict['altitude']
            # check the site frame and set the regions.
            siteframe = SiteFrame.objects.get(pk = settings.XGDS_CURRENT_SITEFRAME_ID)
            # get all the regions for this site frame. 
            regionsForZone = Region.objects.filter(zone = siteframe)
            #self.fields['region'].widget.choices.queryset = regionsForZone
            self.initial['region'] = regionsForZone[0]
            self.fields['region'].empty_label = None
            self.initial['resource'] = GEOCAM_TRACK_RESOURCE_MODEL.get().objects.get(name = settings.XGDS_SAMPLE_DEFAULT_COLLECTOR)
            # auto increment the sample number
            self.initial['number'] = self.instance.getCurrentNumber()
            if self.instance.collection_time:
                utc_collection_time = self.instance.collection_time
            else: 
                utc_collection_time = timezone.now()
            local_time = utcToLocalTime(utc_collection_time) 
            collection_time = local_time.strftime("%m/%d/%Y %H:%M:%S")
            self.initial['collection_time'] = collection_time
    
    
    def clean_year(self):
        year = self.cleaned_data['year']
        if year == None:
            raise forms.ValidationError(u"You haven't set a year.")
        return year
    
    
    def clean_number(self):
        number = self.cleaned_data['number']
        if number == None:
            raise forms.ValidationError(u"You haven't set a number.")
        return number
    
    
    def clean_station_number(self):
        station_number = self.cleaned_data['station_number']
        if station_number == None:
            raise forms.ValidationError(u"You haven't set a station_number.")
        return station_number
    
    
    def clean_collection_timezone(self): 
        try:
            return self.cleaned_data['collection_timezone']
        except:
            return settings.TIME_ZONE
    
    
    def clean_collection_time(self): 
        ctime = self.cleaned_data['collection_time']
        if ctime:  # if there is a time input, convert to utc
            ctimezone = self.clean_collection_timezone()
            tz = pytz.timezone(ctimezone)
            naiveTime = ctime.replace(tzinfo = None)
            localizedTime = tz.localize(naiveTime)
            utcTime = localizedTime.astimezone(pytz.utc)
            ctime = utcTime
        return ctime
    
    
    def clean(self):
        """
        Checks that both lat and lon are entered (or both are empty)
        Checks that collection time is entered if user is entering position for the first time.
        """
        cleaned_data = super(SampleForm, self).clean()
        latitude = cleaned_data.get("latitude")
        longitude = cleaned_data.get("longitude")
        if (latitude and not longitude) or (not latitude and longitude):  # if only one of them is filled in
            msg = "Must enter both latitude and longitude or leave both blank."
            self.add_error('latitude', msg)
            self.add_error('longitude', msg)
        if latitude and longitude:
            instance = super(SampleForm, self).save(commit=False)
            if instance.user_position is None:
                if not self.cleaned_data['collection_time']:
                    msg = "Must enter collection time to record position"
                    self.add_error('collection_time', msg)
                    
                    
    def save(self, commit=True):
        instance = super(SampleForm, self).save(commit=False)
        instance.collection_time = self.cleaned_data['collection_time']
        if instance.resource and instance.collection_time:
            instance.track_position = getClosestPosition(timestamp=instance.collection_time, resource=instance.resource)
        
        if (('latitude' in self.changed_data) and ('longitude' in self.changed_data)) or ('altitude' in self.changed_data):
            if instance.user_position is None:
                instance.user_position = LOCATION_MODEL.get().objects.create(serverTimestamp = datetime.datetime.now(pytz.utc),
                                                                             timestamp = instance.collection_time,
                                                                             latitude = self.cleaned_data['latitude'],
                                                                             longitude = self.cleaned_data['longitude'], 
                                                                             altitude = self.cleaned_data['altitude'])
            else:
                instance.user_position.latitude = self.cleaned_data['latitude']
                instance.user_position.longitude = self.cleaned_data['longitude']
                instance.user_position.altitude = self.cleaned_data['altitude']
        
        if ('collector' in self.changed_data):
            fullName = self.cleaned_data['collector']
            splitName = fullName.split(' ')
            firstAndLast = [x for x in splitName if x.strip()]
            collector = User.objects.filter(first_name=firstAndLast[0]).filter(last_name=firstAndLast[1])[0] 
            instance.collector = collector
        
        # if fields changed, validate against the name
        needsNameRebuild = False
        for field in SAMPLE_MODEL.get().getFieldsForName():
            if field in self.changed_data:
                needsNameRebuild = True
                break
        if needsNameRebuild:
            builtName = instance.buildName()
            if instance.name != builtName:
                instance.name = builtName 

        # if name changed, validate against the fields.
        if 'name' in self.changed_data:
            builtName = instance.buildName()  # name built from the fields.
            nameFromForm = self.cleaned_data['name']
            if nameFromForm != builtName:  
                try: 
                    instance.updateSampleFromName(nameFromForm)
                except: 
                    # if validation fails, return without saving
                    self.errors['error'] = "Save Failed. Name does not validate against the fields. "
                    return instance
        if commit:
            instance.save()
        return instance


    class Meta: 
        model = getModelByName(settings.XGDS_SAMPLE_SAMPLE_MODEL)
        exclude = ['track_position', 
                   'user_position', 
                   'creation_time', 
                   'modification_time', 
                   'creator', 
                   'modifier', 
                   'collector',
                   'label']
