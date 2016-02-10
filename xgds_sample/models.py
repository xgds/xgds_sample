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
from django.db import models
from django.conf import settings
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from geocamUtil.models.AbstractEnum import AbstractEnumModel
from geocamUtil.modelJson import modelToDict
from __builtin__ import classmethod


class Region(models.Model):
    ''' A region is a sub section of an exploration area or zone, ie North Crater'''
    name = models.CharField(max_length=128)
    shortName = models.CharField(max_length=8)
    siteFrameZone = models.CharField(max_length=32)
    siteFrameName = models.CharField(max_length=32)
    siteFrameTimeZone = models.CharField(max_length=64)


class SampleType(AbstractEnumModel):
    pass
    
    
class AbstractSample(models.Model):
    name = models.CharField(max_length=512) # 9 characters
    type = models.ForeignKey(SampleType)
    region = models.ForeignKey(Region)
    location = models.ForeignKey(settings.GEOCAM_TRACK_PAST_POSITION_MODEL, null=True, blank=True)
    collector = models.ForeignKey(User, null=True, blank=True, related_name="%(app_label)s_%(class)s_collector") # person who collected the sample
    creator = models.ForeignKey(User, null=True, blank=True, related_name="%(app_label)s_%(class)s_creator") # person who entered sample data into Minerva
    modifier = models.ForeignKey(User, null=True, blank=True, related_name="%(app_label)s_%(class)s_modifier") # person who entered sample data into Minerva
    collection_time = models.DateTimeField(blank=True, null=True, editable=False)
    creation_time = models.DateTimeField(blank=True, default=datetime.datetime.utcnow(), editable=False)
    modification_time = models.DateTimeField(blank=True, default=datetime.datetime.utcnow(), editable=False)
    
    def buildName(self, inputName):
        name = inputName
        return name
    
    @classmethod
    def createSampleFromName(cls, name):
        pass
    
    @classmethod
    def createSampleFromForm(cls, form):
        pass
    
    def getPrintedLabelURL(self):
        return 'basalt.xgds.org/sample/' + self.name
    
    def toMapDict(self):
        result = modelToDict(self)
        print "result"
        print result
        if result: 
            if self.collection_time:     
                result['collection_time'] = self.collection_time.strftime("%Y-%m-%d %H:%M:%S UTC")
            else: 
                result['collection_time'] = ""
            result['type'] = self.type.display_name
            result['region'] = self.region.name
            result['creator'] = self.creator
            return result
        else: 
            return None
    
    class Meta:
        abstract = True


#class Sample(AbstractSample):
#    pass
            
