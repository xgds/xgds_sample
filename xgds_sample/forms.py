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

from dal import autocomplete

from django.utils import timezone
from django.conf import settings
from django import forms
from django.utils.functional import lazy
from django.contrib.auth.models import User

from django.forms import ModelForm, CharField
from django.core.exceptions import ValidationError
from django.contrib.auth.models import User
from django.db.models import Q

from geocamUtil.loader import getModelByName
from xgds_map_server.models import Place
from xgds_sample.models import SampleType, Label
from geocamUtil.loader import LazyGetModelByName
from geocamUtil.forms.AbstractImportForm import getTimezoneChoices

from geocamTrack.utils import getClosestPosition
from geocamUtil.models import SiteFrame
from geocamUtil.TimeUtil import utcToLocalTime
from xgds_core.forms import SearchForm

LOCATION_MODEL = LazyGetModelByName(settings.GEOCAM_TRACK_PAST_POSITION_MODEL)
SAMPLE_MODEL = LazyGetModelByName(settings.XGDS_SAMPLE_SAMPLE_MODEL)
XGDS_CORE_VEHICLE_MODEL = LazyGetModelByName(settings.XGDS_CORE_VEHICLE_MODEL)
PLACE_FILTER_URL = '/xgds_core/complete/%s.json/' % 'xgds_map_server.Place'

class CollectorCharField(CharField):
    def label_from_instance(self, obj):
        return "TEST LABEL"


class SampleForm(ModelForm):
    lat = forms.FloatField(required=False, label="Latitude")
    lon = forms.FloatField(required=False, label="Longitude")
    altitude = forms.FloatField(required=False, label="Altitude")
    description = forms.CharField(widget=forms.Textarea, required=False, label="Description")
    number = forms.IntegerField(required=False, min_value=0, label="Number", disabled=True)
    station_number = forms.CharField(required=True, label="Station #")
    collector_name = forms.CharField(required=False, label="Collector")
    name = forms.CharField(widget = forms.HiddenInput(), required = False, label="Name", help_text='Name autofills on save.')
    
    hidden_labelNum = forms.IntegerField(widget = forms.HiddenInput(), required = False)
    hidden_name = forms.CharField(widget = forms.HiddenInput(), required = False)
    pk = forms.IntegerField(widget = forms.HiddenInput(), required = False)
    
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
        self.fields['pk'].initial = self.instance.pk
        if self.instance.collector:
            self.fields['collector_name'].initial = self.instance.collector.first_name + ' ' + self.instance.collector.last_name
        positionDict = self.instance.getPositionDict()
        self.fields['lat'].initial = positionDict['lat']
        self.fields['lon'].initial = positionDict['lon']
        if 'altitude' in positionDict:
            self.fields['altitude'].initial = positionDict['altitude']
        if settings.XGDS_MAP_SERVER_DEFAULT_PLACE_ID:
            self.fields['place'].initial = Place.objects.get(id=settings.XGDS_MAP_SERVER_DEFAULT_PLACE_ID)
        self.fields['place'].empty_label = None
        # auto increment the sample number
        self.initial['number'] = self.instance.number
        if not self.instance.number:
            self.initial['number'] = SAMPLE_MODEL.get().getCurrentNumber()
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
        lat = cleaned_data.get("lat")
        lon = cleaned_data.get("lon")
        if (lat and not lon) or (not lat and lon):  # if only one of them is filled in
            msg = "Must enter both latitude and longitude or leave both blank."
            self.add_error('lat', msg)
            self.add_error('lon', msg)
        if lat and lon:
            instance = super(SampleForm, self).save(commit=False)
            if instance.user_position is None:
                if not self.cleaned_data['collection_time']:
                    msg = "Must enter collection time to record position"
                    self.add_error('collection_time', msg)
                    
                    
    def save(self, commit=True):
        instance = super(SampleForm, self).save(commit=False)
        instance.collection_time = self.cleaned_data['collection_time']
        if instance.vehicle and instance.collection_time:
            instance.track_position = getClosestPosition(timestamp=instance.collection_time, vehicle=instance.vehicle)
            
        if (('lat' in self.changed_data) and ('lon' in self.changed_data)) or ('altitude' in self.changed_data):
            if instance.user_position is None:
                instance.user_position = LOCATION_MODEL.get().objects.create(serverTimestamp = datetime.datetime.now(pytz.utc),
                                                                             timestamp = instance.collection_time,
                                                                             latitude = self.cleaned_data['lat'],
                                                                             longitude = self.cleaned_data['lon'], 
                                                                             altitude = self.cleaned_data['altitude'])
            else:
                instance.user_position.latitude = self.cleaned_data['lat']
                instance.user_position.longitude = self.cleaned_data['lon']
                instance.user_position.altitude = self.cleaned_data['altitude']
        
        if ('collector_name' in self.changed_data):
            fullName = self.cleaned_data['collector_name']
            try: 
                splitName = fullName.split(' ')
                firstAndLast = [x for x in splitName if x.strip()]
                collector = User.objects.filter(first_name=firstAndLast[0]).filter(last_name=firstAndLast[1])[0] 
                instance.collector = collector
            except: 
                self.errors['error'] = "Save Failed. User %s does not exist." % fullName
                return instance
        
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


class SearchSampleForm(SearchForm):
    place = forms.ModelChoiceField(Place.objects.all(),
                                   label=settings.XGDS_MAP_SERVER_PLACE_MONIKER,
                                   required=False,
                                   widget=autocomplete.ModelSelect2(url=PLACE_FILTER_URL))

    sample_type = forms.ModelChoiceField(required=False, queryset=SampleType.objects.all())
    label = forms.IntegerField(required=False)
    
    min_collection_time = forms.DateTimeField(input_formats=settings.XGDS_CORE_DATE_FORMATS, required=False, label='Min Time',
                                              widget=forms.DateTimeInput(attrs={'class': 'datetimepicker'}))
    max_collection_time = forms.DateTimeField(input_formats=settings.XGDS_CORE_DATE_FORMATS, required=False, label = 'Max Time',
                                              widget=forms.DateTimeInput(attrs={'class': 'datetimepicker'}))
    
    collection_timezone = forms.ChoiceField(required=False, choices=lazy(getTimezoneChoices, list)(empty=True), 
                                             label='Time Zone', help_text='Required for Min/Max Time')

    
    field_order = SAMPLE_MODEL.get().getSearchFieldOrder()
    
    # populate the times properly
    def clean_min_collection_time(self):
        return self.clean_time('min_collection_time', self.clean_collection_timezone())

    # populate the times properly
    def clean_max_collection_time(self):
        return self.clean_time('max_collection_time', self.clean_collection_timezone())
    
    def clean_collection_timezone(self):
        if self.cleaned_data['collection_timezone'] == 'utc':
            return 'Etc/UTC'
        else:
            return self.cleaned_data['collection_timezone']
        return None

    def clean(self):
        cleaned_data = super(SearchSampleForm, self).clean()
        collection_timezone = cleaned_data.get("collection_timezone")
        min_collection_time = cleaned_data.get("min_collection_time")
        max_collection_time = cleaned_data.get("max_collection_time")

        if min_collection_time or max_collection_time:
            if not collection_timezone:
                self.add_error('event_timezone',"Time Zone is required for min / max times.")
                raise forms.ValidationError(
                    "Time Zone is required for min / max times."
                )
            else:
                del cleaned_data["collection_timezone"]
        return cleaned_data

    def buildQueryForLabel(self, fieldname, field, value):
        return Q(**{fieldname+'__number': int(value)})

    def buildQueryForField(self, fieldname, field, value, minimum=False, maximum=False):
        if fieldname == 'label':
            return self.buildQueryForLabel(fieldname, field, value)
        elif fieldname == 'description' or fieldname == 'name':
            return self.buildContainsQuery(fieldname, field, value)
        return super(SearchSampleForm, self).buildQueryForField(fieldname, field, value, minimum, maximum)
        

    class Meta:
        model = SAMPLE_MODEL.get()
        fields = SAMPLE_MODEL.get().getSearchFormFields()
