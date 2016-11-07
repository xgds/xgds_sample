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
from django.core.urlresolvers import reverse
from geocamUtil.models.AbstractEnum import AbstractEnumModel
from geocamUtil.modelJson import modelToDict
from geocamUtil.UserUtil import getUserName
from django.contrib.auth.models import User

from xgds_core.models import SearchableModel

class Region(models.Model):
    ''' A region is a sub section of an exploration area or zone, ie North Crater'''
    name = models.CharField(max_length=128, db_index=True)
    shortName = models.CharField(max_length=8, db_index=True)
    zone = models.ForeignKey('geocamUtil.SiteFrame', null=True)
    
    def __unicode__(self):
        return u'%s' % (self.name)


class SampleType(AbstractEnumModel):
    
    def __unicode__(self):
        return u'%s' % (self.display_name)
    

class Label(models.Model, SearchableModel):
    number = models.IntegerField(db_index=True)
    url = models.CharField(null=True, max_length=512)    
    last_printed = models.DateTimeField(blank=True, null=True, editable=False, db_index=True)
    
    def __unicode__(self):
        return u'%s' % (self.number)
    
    @property
    def sampleName(self):
        if self.sample:
            if self.sample.name:
                return self.sample.name
        return ''
    
    class Meta:
        ordering = ['number']


DEFAULT_RESOURCE_FIELD = lambda: models.ForeignKey('geocamTrack.Resource', null=True, blank=True)
DEFAULT_TRACK_POSITION_FIELD = lambda: models.ForeignKey('geocamTrack.PastResourcePosition', null=True, blank=True)
DEFAULT_USER_POSITION_FIELD = lambda: models.ForeignKey('geocamTrack.PastResourcePosition', null=True, blank=True, related_name="sample_user_set" )


class AbstractSample(models.Model, SearchableModel):
    name = models.CharField(max_length=64, null=True, blank=True, db_index=True) # 9 characters
    sample_type = models.ForeignKey(SampleType, null=True)
    region = models.ForeignKey(Region, null=True)
    resource = 'set to DEFAULT_RESOURCE_FIELD() or similar in derived classes'
    track_position = 'set to DEFAULT_TRACK_POSITION_FIELD() or similar in derived classes'
    user_position = 'set to DEFAULT_USER_POSITION_FIELD() or similar in derived classes'
    collector = models.ForeignKey(User, null=True, blank=True, related_name="%(app_label)s_%(class)s_collector") # person who collected the sample
    creator = models.ForeignKey(User, null=True, blank=True, related_name="%(app_label)s_%(class)s_creator") # person who entered sample data into Minerva
    modifier = models.ForeignKey(User, null=True, blank=True, related_name="%(app_label)s_%(class)s_modifier") # person who entered sample data into Minerva
    collection_time = models.DateTimeField(blank=True, null=True, editable=False, db_index=True)
    collection_timezone = models.CharField(null=True, blank=False, max_length=128, default=settings.TIME_ZONE, db_index=True)
    creation_time = models.DateTimeField(blank=True, default=timezone.now, editable=False, db_index=True)
    modification_time = models.DateTimeField(blank=True, default=timezone.now, editable=False, db_index=True)
    label = models.OneToOneField(Label, primary_key=True, related_name='sample')
    description = models.CharField(null=True, blank=True, max_length=1024)
    
    @classmethod
    def cls_type(cls):
        return 'Sample'
    
    @property
    def type(self):
        return self.__class__.cls_type()
    
    @classmethod
    def timesearchField(self):
        return 'collection_time'

    @classmethod
    def getFieldOrder(cls):
        return ['label',
                'name',
                'region', 
                'sample_type', 
                'collector_name', 
                'collection_time',
                'description']

    @classmethod
    def getSearchableFields(cls):
        return ['name', 'description', 'collector__first_name', 'collector__last_name', 'sample_type__display_name', 'region__name', 'region__zone__name']
    
    @classmethod
    def getSearchFormFields(cls):
        return ['name',
                'label',
                'sample_type',
                'description',
                'region',
                'resource',
                'collector',
                'creator',
                ]
    
    @classmethod
    def getSearchFieldOrder(cls):
        return ['name',
                'label',
                'sample_type',
                'description',
                'region',
                'resource',
                'collector',
                'creator',
                'collection_timezone',
                'min_collection_time',
                'max_collection_time'
                ]

    @property
    def sample_type_name(self):
        if self.sample_type:
            return self.sample_type.display_name
        return None

    @property
    def label_number(self):
        return int(self.label.number)

    @property
    def region_name(self):
        if self.region:
            return self.region.name
        return None
    
    @property
    def collector_name(self):
        return getUserName(self.collector)

    @property
    def tz(self):
        return self.collection_timezone
    
    @property
    def thumbnail_image_url(self):
        return self.thumbnail_url()

    def thumbnail_time_url(self, event_time):
        return self.thumbnail_url()

    def view_time_url(self, event_time):
        return self.view_url()
    
    def view_url(self):
        return reverse('search_map_single_object', kwargs={'modelPK':self.pk,
                                                           'modelName': settings.XGDS_SAMPLE_SAMPLE_KEY})
    
    def getPosition(self):
        if self.user_position:
            return self.user_position
        if self.track_position:
            return self.track_position
        return None
    
    def thumbnail_url(self):
        # TODO when we have image support for samples return the first image's thumbnail
        return ''
    
    @classmethod
    def getFieldsForName(cls):
        #TODO return a list of fields that will be used to build the name, 
        # to see if they have changed and the name needs updating.
        return []
    
    def buildName(self):
        #TODO implement for your model if you want a custom name
        pass
    
    def updateSampleFromName(self, name):
        #TODO implement for your model if you want fields to change based on name change
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
        result['altitude'] = ''

        if self.user_position:
            result['lat'] = self.user_position.latitude
            result['lon'] = self.user_position.longitude
            if hasattr(self.user_position, 'altitude'):
                result['alt'] = self.user_position.altitude
            return result
        
        result['position_id'] = ''
        if self.track_position:
            result['lat'] = self.track_position.latitude
            result['lon'] = self.track_position.longitude
            if self.track_position.altitude:
                result['alt'] = self.track_position.altitude
            return result
        else: 
            result['lat'] = ''
            result['lon'] = ''
            
        return result
     
    class Meta:
        abstract = True


class SampleLabelSize(models.Model):
    """
    Represents available choices of sample label size.
    """
    name = models.CharField(max_length=80)
    # The label vendor, e.g. Avery
    labelVendor = models.CharField(max_length=80, null=True, blank=True)

    # The label type/model e.g. 5160
    labelType = models.CharField(max_length=80, null=True, blank=True)

    width = models.FloatField(null=True, blank=True)
    height = models.FloatField(null=True, blank=True)
    unit = models.CharField(max_length=16, default="mm")
    orientation = models.CharField(max_length=1, default="L")  # can be L or P for landscape or portrait
    paragraphWidth = models.IntegerField(default=22)

    # python class containing the elements to define this template
    templateElements = models.TextField(null=True, blank=True)
    templateInitialized = False

    def __unicode__(self):
        return '%s (%s %s) (%d%s x %d%s)' % (self.name, self.labelVendor,
                                             self.labelType, self.width, self.unit,
                                             self.height, self.unit)

    def getTemplate(self):
        if not self.templateInitialized:
            if self.unit == "mm":
                mmWidth = self.width
                mmHeight = self.height
            elif self.unit == "in":
                mmWidth = self.width / 0.03937
                mmHeight = self.height / 0.03937

        if self.templateElements:
            elements = getClassByName(self.templateElements)
            if elements:
                template = Template(format=[mmWidth, mmHeight], orientation=self.orientation, elements=elements)
                template.add_page()
                return template

        raise LabelTemplateException("No Template found for label " + self.name)       
