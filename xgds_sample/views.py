# __BEGIN_LICENSE__
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
# __END_LICENSE__
import traceback
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.core.urlresolvers import reverse
from django.http import JsonResponse
from django.template import RequestContext
from django.template.loader import render_to_string

from django.views.decorators.cache import never_cache
from django.conf import settings
from django.contrib import messages 
from django.db.models import Max
from django.utils import timezone
from django.contrib.auth.models import User
from PyPDF2 import PdfFileMerger, PdfFileReader

from datetime import datetime, timedelta
import json
import os
import re
import pytz

from geocamUtil.loader import getClassByName, LazyGetModelByName
from forms import SampleForm
from xgds_data.forms import SearchForm, SpecializedForm
from xgds_sample.models import SampleLabelSize, Region, Label
from xgds_core.views import get_handlebars_templates
from geocamTrack.utils import getClosestPosition
from geocamUtil.models import SiteFrame
from geocamUtil.TimeUtil import utcToLocalTime

from geocamUtil.datetimeJsonEncoder import DatetimeJsonEncoder
from django.views.static import serve
from xgds_sample.labels import *

from django.http import HttpResponse
from StringIO import StringIO


SAMPLE_MODEL = LazyGetModelByName(settings.XGDS_SAMPLE_SAMPLE_MODEL)
LABEL_MODEL = LazyGetModelByName(settings.XGDS_SAMPLE_LABEL_MODEL)

TRACK_MODEL = LazyGetModelByName(settings.GEOCAM_TRACK_TRACK_MODEL)
POSITION_MODEL = LazyGetModelByName(settings.GEOCAM_TRACK_PAST_POSITION_MODEL)
RESOURCE_MODEL = LazyGetModelByName(settings.GEOCAM_TRACK_RESOURCE_MODEL)
ACTIVE_FLIGHT_MODEL = LazyGetModelByName(settings.XGDS_PLANNER2_ACTIVE_FLIGHT_MODEL)

XGDS_SAMPLE_TEMPLATE_LIST = list(settings.XGDS_MAP_SERVER_HANDLEBARS_DIRS)
XGDS_SAMPLE_TEMPLATE_LIST = XGDS_SAMPLE_TEMPLATE_LIST + settings.XGDS_CORE_TEMPLATE_DIRS[settings.XGDS_SAMPLE_SAMPLE_MODEL]
    
# get all user names (string)
def getUserNames():
    allUsers = [user.first_name + ' ' + user.last_name  for user in User.objects.all()]
    allUsers = [str(x) for x in allUsers if x.strip()]
    return allUsers


def getTrackPosition(timestamp, resource):
    '''
    Look up and return the closest tracked position if there is one.
    '''
    return getClosestPosition(timestamp=timestamp, resource=resource)


def deleteLabelAndSample(request, labelNum):
    label = LABEL_MODEL.get().objects.get(number=labelNum)
    message = 'Deleted label %d' % label.number
    try:
        message = message + ' and sample %s ' % label.sample.name
        label.sample.delete()
    except:
        pass
    label.delete()
    messages.error(request, message)
    return render(request, 'xgds_sample/recordSample.html')


def setSampleCustomFields(form, sample):       
    # set custom field values with existing data.
    positionDict = sample.getPositionDict()
    form.fields['latitude'].initial = positionDict['latitude']
    form.fields['longitude'].initial = positionDict['longitude']
    if 'altitude' in positionDict:
        form.fields['altitude'].initial = positionDict['altitude']
    if sample.collection_time:
        form.fields['collection_time'].initial = sample.collection_time
    if sample.collector:
        form.fields['collector'].initial = sample.collector.first_name + ' ' + sample.collector.last_name
    return form


@login_required 
def getSampleEditPage(request, samplePK = None):
    fieldsEnabledFlag = 0  # initially, sample info fields are disabled until user presses enter to submit label number or name
    getSampleInfoUrl = reverse('xgds_sample_get_info')
    sample = None
    sampleMapDict = None
    if samplePK:
        sample = SAMPLE_MODEL.get().objects.get(pk=samplePK)
        fieldsEnabledFlag = 1  # if we get to this page from sample view, enable the fields.
        mapDict = sample.toMapDict()
        sampleMapDict = json.dumps([mapDict], indent=4, cls=DatetimeJsonEncoder)
    form = SampleForm(instance=sample)
    return render(request,
                  'xgds_sample/sampleEdit.html',
                   {'form': form,
                    'users': getUserNames(),
                    'modelName': settings.XGDS_SAMPLE_SAMPLE_KEY,
                    'templates': get_handlebars_templates(list(settings.XGDS_MAP_SERVER_HANDLEBARS_DIRS), 'XGDS_MAP_SERVER_HANDLEBARS_DIRS'),
                    'sampleMapDict': sampleMapDict,
                    'getSampleInfoUrl': getSampleInfoUrl,
                    'fieldsEnabledFlag': fieldsEnabledFlag})
 
 
@login_required
def saveSampleInfo(request):
    getSampleInfoUrl = reverse('xgds_sample_get_info')
    sampleMapDict = None
    if request.method == "POST":
        data = request.POST.dict()
        fieldsEnabledFlag = 1  # input fields can be edited.
        pk = data['pk']
        if pk:
            try:
                sample = SAMPLE_MODEL.get().objects.get(pk=int(pk))
            except:
                sample = None
        else: 
            # create a new sample.
            labelNum = int(data['hidden_labelNum'])
            label, created = LABEL_MODEL.get().objects.get_or_create(number=labelNum)
            sample = SAMPLE_MODEL.get().objects.create(label = label)
        if sample:            
            form = SampleForm(request.POST, instance=sample)
            try:
                if form.is_valid():
                    form.save()
                    fieldsEnabledFlag = 0  # disable fields if successfuly saved.
                    messages.success(request, 'Sample %s successfully updated.' % sample.name)  
            except:
                messages.error(request, 'Sample %s could not be saved.' % sample.name)  
            if form.errors:
                for key, msg in form.errors.items():
                    if key == 'warning':
                        messages.warning(request, msg)
                    elif key == 'error':
                        messages.error(request, msg)
            mapDict = sample.toMapDict()
            sampleMapDict = json.dumps([mapDict], indent=4, cls=DatetimeJsonEncoder)
            form = SampleForm(request.POST)
        return render(request,
                      'xgds_sample/sampleEdit.html',
                       {'form': form,
                        'users': getUserNames(),
                        'modelName': settings.XGDS_SAMPLE_SAMPLE_KEY,
                        'templates': get_handlebars_templates(list(settings.XGDS_MAP_SERVER_HANDLEBARS_DIRS), 'XGDS_MAP_SERVER_HANDLEBARS_DIRS'),
                        'sampleMapDict': sampleMapDict,
                        'getSampleInfoUrl': getSampleInfoUrl,
                        'fieldsEnabledFlag': fieldsEnabledFlag})


def addDefaults(mapDict):
    # set the default information (mirroring forms.py as initial values)
    if 'region_name' not in mapDict or not mapDict['region_name']: 
        mapDict['region_name'] = Region.objects.get(id = settings.XGDS_CURRENT_REGION_ID).name
    if 'number' not in mapDict or not mapDict['number']:
        mapDict['number'] = SAMPLE_MODEL.get().getCurrentNumber()
    # change the server time (UTC) to local time for display
    if 'collection_time' not in mapDict or not mapDict['collection_time']: 
        utc_time = timezone.now() 
    else: 
        utc_time = mapDict['collection_time']
    local_time = utcToLocalTime(utc_time) 
    collection_time = local_time.strftime("%m/%d/%Y %H:%M:%S")
    mapDict['collection_time'] = collection_time
    return mapDict
 
 
def getSampleInfo(request):
    """ 
    When user enters the label number or the sample name, 
    This sends back the associated sample info to populate the 
    edit form. 
    """
    if request.method == "POST":
        postDict = request.POST.dict()
        if 'sampleName' in postDict:
            sampleName = postDict['sampleName']
            if sampleName: 
                try: 
                    sample = SAMPLE_MODEL.get().objects.filter(name=sampleName)[0]
                    mapDict = sample.toMapDict()
                except: 
                    # we no longer support creating sample by name
                    return JsonResponse({'status':'false','message':"Sample %s is not found." % sampleName}, status=500)
        elif 'labelNum' in postDict:
            try: 
                labelNum = int(postDict['labelNum'])
            except: 
                return JsonResponse({'status':'false','message':"Invalid label number %s" % postDict['labelNum']}, status=500)
            if labelNum: 
                defaultResource = None
                try: 
                    notesUserSession = request.session.get('notes_user_session', None)
                    resourceId = int(notesUserSession['resource'])
                    defaultResource = RESOURCE_MODEL.get().objects.get(id = resourceId)
                except: 
                    print "no default resource available."
                try: 
                    sample = SAMPLE_MODEL.get().objects.get(label__number = labelNum)
                    if defaultResource:
                        sample.setExtrasDefault(defaultResource)
                    mapDict = sample.toMapDict()
                except: 
                    # sample does not exist yet. Proceed.
                    year = timezone.now().year % 2000
                    mapDict = {'label_number': labelNum, 'collection_timezone': settings.TIME_ZONE, 
                               'pk': '', 'year': year}
                    if defaultResource: 
                        mapDict['resource_name'] = defaultResource.name
                        foundActiveFlights = ACTIVE_FLIGHT_MODEL.get().objects.filter(flight__vehicle = defaultResource.vehicle)
                        if foundActiveFlights: 
                            defaultFlight = foundActiveFlights[0].flight
                            mapDict['flight'] = defaultFlight.name
                
        try: 
            mapDict = addDefaults(mapDict)
            json_data = json.dumps([mapDict], indent=4, cls=DatetimeJsonEncoder)
            return HttpResponse(json_data, content_type='application/json', status=200)
        except: 
            traceback.print_exc()
            return JsonResponse({'status':'false','message':'Sample info is not in proper JSON format'}, status=500)
    else: 
        return JsonResponse({'status':'false','message':'Request method %s not supported.' % request.method}, status=500)
                    
    
@login_required
def getSampleLabelsPage(request):
    labels = LABEL_MODEL.get().objects.all()
    return render(request,
                  'xgds_sample/sampleLabels.html',
                  {'labels': labels,
                   'file_url': ""})


def chunks(l, n):
    n = max(1, n)
    return [l[i:i + n] for i in range(0, len(l), n)]


def printSampleLabels(request):
    data = {'file_url': ""}
    if request.method == 'POST': 
        if 'label_quantity' in request.POST:
            quantity = int(request.POST['label_quantity'])
            if quantity <= 0:
                messages.error(request, "Quantity must be an integer greater than 0.")
                return render(request, 'xgds_sample/sampleLabels.html') 
            labels = LABEL_MODEL.get().getAvailableLabels()
            labelNumbers = [label.number for label in labels]
            
            # if there are lots of available label numbers, get just the number specified in 'quantity'
            labelNumbers = labelNumbers[:quantity]

            # if there are not enough label numbers, add more
            for x in range(quantity - len(labelNumbers)): 
                labelNumbers.append(labelNumbers[-1] + 1)
            
            labelsToPrint = []
            for labelNum in labelNumbers: 
                label, create = LABEL_MODEL.get().objects.get_or_create(number=int(labelNum))
                labelsToPrint.append(label)
        else: 
            labelIds = request.POST.getlist('label_checkbox')
            intLabelIds = [int(labelId) for labelId in labelIds]
            labelsToPrint = LABEL_MODEL.get().objects.filter(id__in=intLabelIds)
        if labelsToPrint:
            size = SampleLabelSize.objects.get(name="small")
            labelChunks = chunks(labelsToPrint, 10)  # labels in chunks of 10. (list of lists)
            pdfFileNames = []
            index = 0
            for labelChunk in labelChunks: 
                pdfFileName = generateMultiPDF(labelChunk, size, index)
                pdfFileNames.append(pdfFileName)
                index = index + 1
            
            # merge the single sheet of pdf files into one to create multiple page pdf.
            merger = PdfFileMerger()
            outputFileName = re.sub(r"_temp\d+", "", pdfFileNames[0])
            for filename in pdfFileNames:
                merger.append(PdfFileReader(file(filename, 'rb')))
                # delete the temporary file
                os.remove(filename)
            merger.write(outputFileName)  # merge them into one file, and take the first file's name

            outputFileName = outputFileName.replace(settings.DATA_ROOT, settings.DATA_URL)
            messages.success(request, "Labels successfully generated.")
            data['file_url'] = outputFileName         
    return render(request,'xgds_sample/sampleLabels.html', data) 
    

def getSampleHelpPage(request):
    image1Url = settings.STATIC_URL + 'xgds_sample/images/Slide1.png'
    image2Url = settings.STATIC_URL + 'xgds_sample/images/Slide2.png'
    image3Url = settings.STATIC_URL + 'xgds_sample/images//Slide3.png'
    data = {'image1': image1Url,
            'image2': image2Url, 
            'image3': image3Url}
    return render(request, 'xgds_sample/sampleHelp.html', data) 
    

if settings.XGDS_NOTES_ENABLE_GEOCAM_TRACK_MAPPING:
    from geocamUtil.KmlUtil import wrapKmlDjango, djangoResponse

    def getKmlNetworkLink(request):
        url = request.build_absolute_uri(settings.SCRIPT_NAME + 'xgds_sample/rest/samples.kml')
        return djangoResponse('''
    <NetworkLink>
      <name>%(name)s</name>
      <Link>
        <href>%(url)s</href>
        <refreshMode>onInterval</refreshMode>
        <refreshInterval>5</refreshInterval>
      </Link>
    </NetworkLink>
    ''' % dict(name=settings.XGDS_SAMPLE_SAMPLE_KEY + 's',
               url=url))

    @never_cache
    def sample_map_kml(request, range=12):
        now = datetime.now(pytz.utc)
        yesterday = now - timedelta(seconds=3600 * range)
        objects = SAMPLE_MODEL.get().objects.filter(collection_time__lte=now).filter(collection_time__gte=yesterday)
        days = []
        if objects:
            days.append({'date': now,
                        'samples': objects
                        })

        if days:
            kml_document = render_to_string('xgds_sample/samples_placemark_document.kml',
                                            {'days': days,
                                             'iconUrl': request.build_absolute_uri('/static/rest/xgds_sample/images/sample_icon.png')},
                                            request)
            return wrapKmlDjango(kml_document)
        return wrapKmlDjango("")

