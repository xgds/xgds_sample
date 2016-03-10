#__BEGIN_LICENSE__
# Copyright (c) 2015, United States Government, as represented by the
# Administrator of the National Aeronautics and Space Administration.
# All rights reserved.
#
# The xGDS platform is licensed under the Apache License, Version 2.0
# (the "License"); you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
# http://www.apache.org/licenses/LICENSE-2.0.I
#
# Unless required by applicable law or agreed to in writing, software distributed
# under the License is distributed on an "AS IS" BASIS, WITHOUT WARRANTIES OR
# CONDITIONS OF ANY KIND, either express or implied. See the License for the
# specific language governing permissions and limitations under the License.
#__END_LICENSE__

import datetime
import pytz
from django.utils import timezone

from django.db import models
from django.conf import settings
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from geocamUtil.models.AbstractEnum import AbstractEnumModel
from geocamUtil.modelJson import modelToDict
from geocamUtil.UserUtil import getUserName

class Region(models.Model):
    ''' A region is a sub section of an exploration area or zone, ie North Crater'''
    name = models.CharField(max_length=128)
    shortName = models.CharField(max_length=8)
    siteFrameZone = models.CharField(max_length=32)
    siteFrameName = models.CharField(max_length=32)
    siteFrameTimeZone = models.CharField(max_length=64)
    
    def __unicode__(self):
        return u'%s' % (self.name)


class SampleType(AbstractEnumModel):
    
    def __unicode__(self):
        return u'%s' % (self.display_name)
    

class Label(models.Model):
    number = models.IntegerField()
    url = models.CharField(null=True, max_length=512)    
    last_printed = models.DateTimeField(blank=True, null=True, editable=False)
    
    def __unicode__(self):
        return u'%s' % (self.number)
    
    def toMapDict(self):
        result = modelToDict(self)
        try:
            result['sampleName'] = self.sample.name
        except: 
            result['sampleName'] = ""
        return result

     
class AbstractSample(models.Model):
    name = models.CharField(max_length=512, null=True) # 9 characters
    type = models.ForeignKey(SampleType, null=True)
    region = models.ForeignKey(Region, null=True)
    resource = models.ForeignKey(settings.GEOCAM_TRACK_RESOURCE_MODEL, null=True, blank=True)
    track_position = models.ForeignKey(settings.GEOCAM_TRACK_PAST_POSITION_MODEL, null=True, blank=True)
    user_position = models.ForeignKey(settings.GEOCAM_TRACK_PAST_POSITION_MODEL, null=True, blank=True, related_name="sample_user_set" )
    collector = models.ForeignKey(User, null=True, blank=True, related_name="%(app_label)s_%(class)s_collector") # person who collected the sample
    creator = models.ForeignKey(User, null=True, blank=True, related_name="%(app_label)s_%(class)s_creator") # person who entered sample data into Minerva
    modifier = models.ForeignKey(User, null=True, blank=True, related_name="%(app_label)s_%(class)s_modifier") # person who entered sample data into Minerva
    collection_time = models.DateTimeField(blank=True, null=True, editable=False)
    collection_timezone = models.CharField(null=True, blank=False, max_length=128, default=settings.TIME_ZONE)
    creation_time = models.DateTimeField(blank=True, default=timezone.now, editable=False)
    modification_time = models.DateTimeField(blank=True, default=timezone.now, editable=False)
    label = models.OneToOneField(Label, primary_key=True, related_name='sample')
    
    def buildName(self):
        pass
    
    def updateSampleFromName(self, name):
        pass
    
    def finish_initialization(self, request):
        ''' during construction, if you have extra data to fill in you can override this method'''
        pass
    
    def getPositionDict(self):
        ''' override if you want to change the logic for how the positions are prioritized in JSON.
        Right now track_position is from the track, and user_position stores any hand edits.
        track provides lat lon and altitude and heading, and user trumps all.
        '''
        result = {}
        result['altitude'] = ""

        if self.user_position:
            result['lat'] = self.user_position.latitude
            result['lon'] = self.user_position.longitude
            if hasattr(self.user_position, 'altitude'):
                result['altitude'] = self.user_position.altitude
            return result
        
        result['position_id'] = ""
        if self.track_position:
            result['lat'] = self.track_position.latitude
            result['lon'] = self.track_position.longitude
            if self.track_position.altitude:
                result['altitude'] = self.track_position.altitude
            return result
        else: 
            result['lat'] = ""
            result['lon'] = ""
            
        return result
    
    def toMapDict(self):
        result = modelToDict(self)
        if result: 
            if self.collector:
                result['collector'] = getUserName(self.collector)
            if self.collection_time:     
                result['collection_time'] = self.collection_time.strftime("%m/%d/%Y %H:%M")
            else: 
                result['collection_time'] = ""
            result.update(self.getPositionDict())
            return result
        else: 
            return None
    
    class Meta:
        abstract = True

            
