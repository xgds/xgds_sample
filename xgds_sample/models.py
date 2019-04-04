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

from django.utils import timezone

from django.db import models
from django.db.models import Max
from django.conf import settings
from django.core.exceptions import ObjectDoesNotExist
from django.core.urlresolvers import reverse
from geocamUtil.models.AbstractEnum import AbstractEnumModel
from geocamUtil.UserUtil import getUserName
from django.contrib.auth.models import User
from django.urls import reverse

from xgds_core.models import SearchableModel, IsFlightChild, IsFlightData, BroadcastMixin
from xgds_notes2.models import NoteMixin, NoteLinksMixin, DEFAULT_NOTES_GENERIC_RELATION

from geocamUtil.loader import LazyGetModelByName
from geocamUtil.models.ExtrasDotField import ExtrasDotField

from xgds_map_server.models import Place

import json
from django.db.models.signals import post_save
from django.dispatch import receiver
if settings.XGDS_CORE_REDIS:
    from xgds_core.redisUtil import publishRedisSSE


class SampleType(AbstractEnumModel):
    
    def __unicode__(self):
        return u'%s' % (self.display_name)


def get_next_label_number():
    """
    Get the next unused label number, or 1 if none exist
    :return:
    """
    try:
        max_dict = Label.objects.all().aggregate(Max('number'))
        max_value = max_dict['number__max']
        if max_value:
            return max_value + 1
        else:
            return 1
    except ObjectDoesNotExist:
        return 1


class Label(models.Model, SearchableModel):

    number = models.IntegerField(db_index=True, unique=True, default=get_next_label_number)
    url = models.CharField(null=True, max_length=512)    
    last_printed = models.DateTimeField(blank=True, null=True, editable=False, db_index=True)
    
    def __unicode__(self):
        return u'%s' % self.number
    
    @property
    def sampleName(self):
        if self.sample:
            if self.sample.name:
                return self.sample.name
        return ''
    
    @classmethod
    def getAvailableLabels(cls):
        return cls.objects.filter(sample__name__isnull=True)

    class Meta:
        ordering = ['number']

#TODO if you are are not using any of these default types be sure to customize these fields.
DEFAULT_VEHICLE_FIELD = lambda: models.ForeignKey('xgds_core.Vehicle', null=True, blank=True)
DEFAULT_TRACK_POSITION_FIELD = lambda: models.ForeignKey(settings.GEOCAM_TRACK_PAST_POSITION_MODEL, null=True, blank=True, related_name="%(app_label)s_%(class)s_track_position")
DEFAULT_USER_POSITION_FIELD = lambda: models.ForeignKey(settings.GEOCAM_TRACK_PAST_POSITION_MODEL, null=True, blank=True, related_name="%(app_label)s_%(class)s_user_position" )
DEFAULT_FLIGHT_FIELD = lambda: models.ForeignKey('xgds_core.Flight', related_name='%(app_label)s_%(class)s_related',
                                                 verbose_name=settings.XGDS_CORE_FLIGHT_MONIKER, blank=True, null=True)


class AbstractSample(models.Model, SearchableModel, IsFlightChild, IsFlightData, NoteMixin, NoteLinksMixin,
                     BroadcastMixin):
    name = models.CharField(max_length=64, null=True, blank=True, db_index=True) # 9 characters
    sample_type = models.ForeignKey(SampleType, null=True)
    place = models.ForeignKey(Place, null=True, verbose_name=settings.XGDS_MAP_SERVER_PLACE_MONIKER)
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
    flight = "TODO set to DEFAULT_FLIGHT_FIELD or similar"
    extras = ExtrasDotField(default='')

    @classmethod
    def get_tree_json(cls, parent_class, parent_pk):
        try:
            found = LazyGetModelByName(settings.XGDS_SAMPLE_SAMPLE_MODEL).get().objects.filter(flight__id=parent_pk)
            result = None
            if found.exists():
                moniker = settings.XGDS_SAMPLE_SAMPLE_MONIKER + 's'
                flight = found[0].flight
                result = [{"title": moniker,
                           "selected": False,
                           "tooltip": "%s for %s " % (moniker, flight.name),
                           "key": "%s_%s" % (flight.uuid, moniker),
                           "data": {"json": reverse('xgds_map_server_objectsJson',
                                                    kwargs={'object_name': 'XGDS_SAMPLE_SAMPLE_MODEL',
                                                            'filter': 'flight__pk:' + str(flight.pk)}),
                                    "sseUrl": "",
                                    "type": 'MapLink',
                                    }
                           }]
            return result
        except ObjectDoesNotExist:
            return None

    @classmethod
    def get_info_json(cls, flight_pk):
        found = LazyGetModelByName(settings.XGDS_SAMPLE_SAMPLE_MODEL).get().objects.filter(flight__id=flight_pk)
        result = None
        if found.exists():
            flight = LazyGetModelByName(settings.XGDS_CORE_FLIGHT_MODEL).get().objects.get(id=flight_pk)
            result = {'name': settings.XGDS_SAMPLE_SAMPLE_MONIKER + 's',
                      'count': found.count(),
                      'url': reverse('search_map_object_filter',
                                     kwargs={'modelName': settings.XGDS_SAMPLE_SAMPLE_MONIKER,
                                             'filter': 'flight__group:%d,flight__vehicle:%d' % (
                                             flight.group.pk, flight.vehicle.pk)})
                      }
        return result

    def __unicode__(self):
        return u'%s' % (self.name)

    @classmethod
    def cls_type(cls):
        return settings.XGDS_SAMPLE_SAMPLE_KEY
    
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
                'place',
                'sample_type', 
                'collector_name', 
                'collection_time',
                'description']

    @classmethod
    def getSearchableFields(cls):
        return ['name',
                'description',
                'collector__first_name',
                'collector__last_name',
                'sample_type__display_name',
                'place__name',
                'place__region__name',
                'extras']
    
    @classmethod
    def getSearchFormFields(cls):
        return ['name',
                'label',
                'sample_type',
                'description',
                'place',
                'flight__vehicle',
                'flight',
                'collector',
                'creator',
                ]
    
    @classmethod
    def getSearchFieldOrder(cls):
        return ['name',
                'label',
                'sample_type',
                'description',
                'place',
                #'vehicle',
                'flight',
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
    def place_name(self):
        if self.place:
            return self.place.name
        return None

    @classmethod
    def place_label(cls):
        return settings.XGDS_MAP_SERVER_PLACE_MONIKER

    @property
    def collector_name(self):
        return getUserName(self.collector)

    @property
    def collector_pk(self):
        if self.collector:
            return self.collector.pk
        return None

    @property
    def id(self):
        return self.pk

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
    
    def setExtrasDefault(self, defaultVehicle):
        ''' If the sample does not have vehicle, set it with the default vehicle'''
        if not self.vehicle:
            if defaultVehicle:
                self.vehicle = defaultVehicle
                self.save()
    
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

    @classmethod
    def get_time_bounds_field_name(cls):
        """
        If your min/max time search field differs from this name override this method.
        :return:
        """
        return 'collection_time'
     
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


class Sample(AbstractSample):
    """
    Sample sample class
    TODO: ensure it is minimal viable model
    """

    track_position = DEFAULT_TRACK_POSITION_FIELD()
    user_position = DEFAULT_USER_POSITION_FIELD()
    flight = DEFAULT_FLIGHT_FIELD()
    notes = DEFAULT_NOTES_GENERIC_RELATION()

# @receiver(post_save, sender=Sample)
# def publishAfterSave(sender, instance, **kwargs):
#     if settings.XGDS_CORE_REDIS:
#         for channel in settings.XGDS_SSE_SAMPLE_CHANNELS:
#             publishRedisSSE(channel, settings.XGDS_SAMPLE_SSE_TYPE.lower(), json.dumps({}))

