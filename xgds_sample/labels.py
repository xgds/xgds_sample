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

from datetime import datetime
import qrcode
import textwrap
import os
from fpdf import Template

from django.conf import settings
from xgds_sample import labelTemplates
from geocamUtil.loader import LazyGetModelByName


SAMPLE_MODEL = LazyGetModelByName(settings.XGDS_SAMPLE_SAMPLE_MODEL)

def generateMultiPDF(sampleLabels, size):
    """
    Actually create the PDF for multiple sample labels.
    """
    now = datetime.utcnow()
    printableFile = "multi_" + size.name + "_" + now.strftime("%Y%m%d_%H%M%S") + ".pdf"

    # clear out any old version
    outputFilename = os.path.join(settings.MEDIA_ROOT, settings.XGDS_SAMPLE_PDF_DIR, printableFile)

    # get the template
    elements = getattr(labelTemplates, 'multi' + size.name)
    template = Template(format=[215.9, 279.4], orientation="P", elements=elements)
    template.add_page()

    qrCodeImages = []

    i = 0
    paragraph = size.paragraphWidth
    
    for sampleLabel in sampleLabels:
        if i == 10:
            break

        # make the qr code image
        qrCodeImages.append(generateQRCode(sampleLabel.url, sampleLabel.number))

        # populate the templatto ae
        template[str(i) + "_qrcode"] = qrCodeImages[i]
        
        if sampleLabel.number:
            template[str(i) + "_id"] = sampleLabel.number

        try: 
            sample = sampleLabel.sample
        except: 
            sample = None

        # display description next to the qr code
        if sample:
            rows = [sample.name]
            if sample.description:
                rows.append(sample.description)
            samplePosition = sample.getPositionDict()
            if samplePosition:
                if samplePosition['lat'] and samplePosition['lon']:
                    rows.append('lat, lon: ' + samplePosition['lat'] + ' ' + samplePosition['lon'])
            if sample.collection_time: 
                rows.append('collected at ' + sample.collection_time.strftime('%Y-%m-%d %H:%i %e'))
            finalrows = []
            for row in rows:
                if len(row) > paragraph:
                    wrapped = textwrap.wrap(row, paragraph)
                    for l in wrapped:
                        finalrows.append(l)
                else:
                    finalrows.append(row)
    
            for j, row in enumerate(finalrows):
                key = "%d_row%d" % (i, j + 1)
                if (key) in template.keys:
                    template[key] = row
        # update the record.  This is also a lie, we don't know if you actually printed it, but whatever.
        sampleLabel.printTime = now
        sampleLabel.printableFile = printableFile
        sampleLabel.save()
        i = i + 1
        
    while i < 10:
        template[str(i) + "_qrcode"] = os.path.join(settings.STATIC_ROOT, "xgds_sample/images/ipx.gif")
        i = i + 1

    # make the PDF
    template.render(outputFilename)

    # remove the qr code image
    for qrCodeImage in qrCodeImages:
        os.remove(qrCodeImage)

    return outputFilename


def generateQRCode(data, label_id):
    """
    Create a qr code image for this sample.
    Right now these are a fixed size.
    """
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=6,  # how many pixels each box is
        border=4,  # 4 is the minimum # of boxes for the border
    )
    qr.add_data(data)
    qr.make(fit=True)

    img = qr.make_image()
    filename = "qrcode_%d.png" % label_id
    imgFilename = os.path.join(settings.MEDIA_ROOT, settings.XGDS_SAMPLE_PDF_DIR, filename)
    img.save(imgFilename)
    return imgFilename