# __BEGIN_LICENSE__
#Copyright (c) 2015, United States Government, as represented by the 
#Administrator of the National Aeronautics and Space Administration. 
#All rights reserved.
#
#The xGDS platform is licensed under the Apache License, Version 2.0 
#(the "License"); you may not use this file except in compliance with the License. 
#You may obtain a copy of the License at 
#http://www.apache.org/licenses/LICENSE-2.0.
#
#Unless required by applicable law or agreed to in writing, software distributed 
#under the License is distributed on an "AS IS" BASIS, WITHOUT WARRANTIES OR 
#CONDITIONS OF ANY KIND, either express or implied. See the License for the 
#specific language governing permissions and limitations under the License.
# __END_LICENSE__

""" see https://code.google.com/p/pyfpdf/wiki/Templates
"""

#this will define the ELEMENTS that will compose the template for a small label, assuming width = 3 height = 2 inches, sizes in mm
small = [
    {'name': 'qrcode', 'type': 'I', 'x1': 7, 'y1': 15, 'x2': 47, 'y2': 55, 'font': None, 'size': 0.0, 'bold': 0, 'italic': 0, 'underline': 0, 'foreground': 0, 'background': 0xFFFFFF, 'align': 'L', 'text': '', 'priority': 2, },
    {'name': 'id', 'type': 'T', 'x1': 7, 'y1': 55, 'x2': 47, 'y2': 58, 'font': 'Arial', 'size': 20.0, 'bold': 1, 'italic': 0, 'underline': 0, 'foreground': 0, 'background': 0xFFFFFF, 'align': 'C', 'text': '', 'priority': 2, },
    {'name': 'row1', 'type': 'T', 'x1': 45, 'y1': 15, 'x2': 108, 'y2': 30, 'font': 'Arial', 'size': 18.0, 'bold': 1, 'italic': 0, 'underline': 0, 'foreground': 0, 'background': 0xFFFFFF, 'align': 'L', 'text': '', 'priority': 2, },
    {'name': 'row2', 'type': 'T', 'x1': 45, 'y1': 29, 'x2': 108, 'y2': 34, 'font': 'Arial', 'size': 12.0, 'bold': 0, 'italic': 0, 'underline': 0, 'foreground': 0, 'background': 0xFFFFFF, 'align': 'L', 'text': '', 'priority': 2, },
    {'name': 'row3', 'type': 'T', 'x1': 45, 'y1': 34, 'x2': 108, 'y2': 39, 'font': 'Arial', 'size': 12.0, 'bold': 0, 'italic': 0, 'underline': 0, 'foreground': 0, 'background': 0xFFFFFF, 'align': 'L', 'text': '', 'priority': 2, },
    {'name': 'row4', 'type': 'T', 'x1': 45, 'y1': 39, 'x2': 108, 'y2': 44, 'font': 'Arial', 'size': 12.0, 'bold': 0, 'italic': 0, 'underline': 0, 'foreground': 0, 'background': 0xFFFFFF, 'align': 'L', 'text': '', 'priority': 2, },
]

#this will define the elements that will compose the template for a medium label
medium = [
    {'name': 'qrcode', 'type': 'I', 'x1': 7, 'y1': 15, 'x2': 47, 'y2': 55, 'font': None, 'size': 0.0, 'bold': 0, 'italic': 0, 'underline': 0, 'foreground': 0, 'background': 0xFFFFFF, 'align': 'L', 'text': '', 'priority': 2, },
    {'name': 'id', 'type': 'T', 'x1': 7, 'y1': 55, 'x2': 47, 'y2': 58, 'font': 'Arial', 'size': 20.0, 'bold': 1, 'italic': 0, 'underline': 0, 'foreground': 0, 'background': 0xFFFFFF, 'align': 'C', 'text': '', 'priority': 2, },
    {'name': 'row1', 'type': 'T', 'x1': 45, 'y1': 15, 'x2': 103, 'y2': 30, 'font': 'Arial', 'size': 18.0, 'bold': 1, 'italic': 0, 'underline': 0, 'foreground': 0, 'background': 0xFFFFFF, 'align': 'L', 'text': '', 'priority': 2, },
    {'name': 'row2', 'type': 'T', 'x1': 45, 'y1': 28, 'x2': 103, 'y2': 35, 'font': 'Arial', 'size': 18.0, 'bold': 1, 'italic': 0, 'underline': 0, 'foreground': 0, 'background': 0xFFFFFF, 'align': 'L', 'text': '', 'priority': 2, },
    {'name': 'row3', 'type': 'T', 'x1': 45, 'y1': 40, 'x2': 103, 'y2': 45, 'font': 'Arial', 'size': 12.0, 'bold': 0, 'italic': 0, 'underline': 0, 'foreground': 0, 'background': 0xFFFFFF, 'align': 'L', 'text': '', 'priority': 2, },
    {'name': 'row4', 'type': 'T', 'x1': 45, 'y1': 45, 'x2': 103, 'y2': 50, 'font': 'Arial', 'size': 12.0, 'bold': 0, 'italic': 0, 'underline': 0, 'foreground': 0, 'background': 0xFFFFFF, 'align': 'L', 'text': '', 'priority': 2, },
    {'name': 'row5', 'type': 'T', 'x1': 45, 'y1': 50, 'x2': 103, 'y2': 55, 'font': 'Arial', 'size': 12.0, 'bold': 0, 'italic': 0, 'underline': 0, 'foreground': 0, 'background': 0xFFFFFF, 'align': 'L', 'text': '', 'priority': 2, },
    {'name': 'row6', 'type': 'T', 'x1': 45, 'y1': 55, 'x2': 103, 'y2': 60, 'font': 'Arial', 'size': 12.0, 'bold': 0, 'italic': 0, 'underline': 0, 'foreground': 0, 'background': 0xFFFFFF, 'align': 'L', 'text': '', 'priority': 2, },
    {'name': 'row7', 'type': 'T', 'x1': 45, 'y1': 60, 'x2': 103, 'y2': 65, 'font': 'Arial', 'size': 12.0, 'bold': 0, 'italic': 0, 'underline': 0, 'foreground': 0, 'background': 0xFFFFFF, 'align': 'L', 'text': '', 'priority': 2, },
    {'name': 'row8', 'type': 'T', 'x1': 45, 'y1': 65, 'x2': 103, 'y2': 70, 'font': 'Arial', 'size': 12.0, 'bold': 0, 'italic': 0, 'underline': 0, 'foreground': 0, 'background': 0xFFFFFF, 'align': 'L', 'text': '', 'priority': 2, },
    {'name': 'row9', 'type': 'T', 'x1': 45, 'y1': 70, 'x2': 103, 'y2': 75, 'font': 'Arial', 'size': 12.0, 'bold': 0, 'italic': 0, 'underline': 0, 'foreground': 0, 'background': 0xFFFFFF, 'align': 'L', 'text': '', 'priority': 2, },
]

# this is for the multi template for the medium labels, avery 5524
multimedium = [
    # top margin 12.7
    # left  = 4
    # right margin 4.7625
    # bottom margin 12.7
    # center gutter 4.7625
    # 6 labels per sheet

    {'name': '0_qrcode', 'type': 'I', 'x1': 7, 'y1': 15, 'x2': 47, 'y2': 55, 'font': None, 'size': 0.0, 'bold': 0, 'italic': 0, 'underline': 0, 'foreground': 0, 'background': 0xFFFFFF, 'align': 'L', 'text': '', 'priority': 2, },
    {'name': '0_id', 'type': 'T', 'x1': 7, 'y1': 55, 'x2': 47, 'y2': 58, 'font': 'Arial', 'size': 20.0, 'bold': 1, 'italic': 0, 'underline': 0, 'foreground': 0, 'background': 0xFFFFFF, 'align': 'C', 'text': '', 'priority': 2, },
    {'name': '0_row1', 'type': 'T', 'x1': 45, 'y1': 15, 'x2': 103, 'y2': 30, 'font': 'Arial', 'size': 18.0, 'bold': 1, 'italic': 0, 'underline': 0, 'foreground': 0, 'background': 0xFFFFFF, 'align': 'L', 'text': '', 'priority': 2, },
    {'name': '0_row2', 'type': 'T', 'x1': 45, 'y1': 28, 'x2': 103, 'y2': 35, 'font': 'Arial', 'size': 18.0, 'bold': 1, 'italic': 0, 'underline': 0, 'foreground': 0, 'background': 0xFFFFFF, 'align': 'L', 'text': '', 'priority': 2, },
    {'name': '0_row3', 'type': 'T', 'x1': 45, 'y1': 40, 'x2': 103, 'y2': 45, 'font': 'Arial', 'size': 12.0, 'bold': 0, 'italic': 0, 'underline': 0, 'foreground': 0, 'background': 0xFFFFFF, 'align': 'L', 'text': '', 'priority': 2, },
    {'name': '0_row4', 'type': 'T', 'x1': 45, 'y1': 45, 'x2': 103, 'y2': 50, 'font': 'Arial', 'size': 12.0, 'bold': 0, 'italic': 0, 'underline': 0, 'foreground': 0, 'background': 0xFFFFFF, 'align': 'L', 'text': '', 'priority': 2, },
    {'name': '0_row5', 'type': 'T', 'x1': 45, 'y1': 50, 'x2': 103, 'y2': 55, 'font': 'Arial', 'size': 12.0, 'bold': 0, 'italic': 0, 'underline': 0, 'foreground': 0, 'background': 0xFFFFFF, 'align': 'L', 'text': '', 'priority': 2, },
    {'name': '0_row6', 'type': 'T', 'x1': 45, 'y1': 55, 'x2': 103, 'y2': 60, 'font': 'Arial', 'size': 12.0, 'bold': 0, 'italic': 0, 'underline': 0, 'foreground': 0, 'background': 0xFFFFFF, 'align': 'L', 'text': '', 'priority': 2, },
    {'name': '0_row7', 'type': 'T', 'x1': 45, 'y1': 60, 'x2': 103, 'y2': 65, 'font': 'Arial', 'size': 12.0, 'bold': 0, 'italic': 0, 'underline': 0, 'foreground': 0, 'background': 0xFFFFFF, 'align': 'L', 'text': '', 'priority': 2, },
    {'name': '0_row8', 'type': 'T', 'x1': 45, 'y1': 65, 'x2': 103, 'y2': 70, 'font': 'Arial', 'size': 12.0, 'bold': 0, 'italic': 0, 'underline': 0, 'foreground': 0, 'background': 0xFFFFFF, 'align': 'L', 'text': '', 'priority': 2, },
    {'name': '0_row9', 'type': 'T', 'x1': 45, 'y1': 70, 'x2': 103, 'y2': 75, 'font': 'Arial', 'size': 12.0, 'bold': 0, 'italic': 0, 'underline': 0, 'foreground': 0, 'background': 0xFFFFFF, 'align': 'L', 'text': '', 'priority': 2, },

    {'name': '1_qrcode', 'type': 'I', 'x1': 7, 'y1': 93, 'x2': 47, 'y2': 133, 'font': None, 'size': 0.0, 'bold': 0, 'italic': 0, 'underline': 0, 'foreground': 0, 'background': 0xFFFFFF, 'align': 'L', 'text': '', 'priority': 2, },
    {'name': '1_id', 'type': 'T', 'x1': 7, 'y1': 133, 'x2': 47, 'y2': 136, 'font': 'Arial', 'size': 20.0, 'bold': 1, 'italic': 0, 'underline': 0, 'foreground': 0, 'background': 0xFFFFFF, 'align': 'C', 'text': '', 'priority': 2, },
    {'name': '1_row1', 'type': 'T', 'x1': 45, 'y1': 93, 'x2': 103, 'y2': 108, 'font': 'Arial', 'size': 18.0, 'bold': 1, 'italic': 0, 'underline': 0, 'foreground': 0, 'background': 0xFFFFFF, 'align': 'L', 'text': '', 'priority': 2, },
    {'name': '1_row2', 'type': 'T', 'x1': 45, 'y1': 108, 'x2': 103, 'y2': 113, 'font': 'Arial', 'size': 18.0, 'bold': 1, 'italic': 0, 'underline': 0, 'foreground': 0, 'background': 0xFFFFFF, 'align': 'L', 'text': '', 'priority': 2, },
    {'name': '1_row3', 'type': 'T', 'x1': 45, 'y1': 118, 'x2': 103, 'y2': 123, 'font': 'Arial', 'size': 12.0, 'bold': 0, 'italic': 0, 'underline': 0, 'foreground': 0, 'background': 0xFFFFFF, 'align': 'L', 'text': '', 'priority': 2, },
    {'name': '1_row4', 'type': 'T', 'x1': 45, 'y1': 123, 'x2': 103, 'y2': 128, 'font': 'Arial', 'size': 12.0, 'bold': 0, 'italic': 0, 'underline': 0, 'foreground': 0, 'background': 0xFFFFFF, 'align': 'L', 'text': '', 'priority': 2, },
    {'name': '1_row5', 'type': 'T', 'x1': 45, 'y1': 128, 'x2': 103, 'y2': 133, 'font': 'Arial', 'size': 12.0, 'bold': 0, 'italic': 0, 'underline': 0, 'foreground': 0, 'background': 0xFFFFFF, 'align': 'L', 'text': '', 'priority': 2, },
    {'name': '1_row6', 'type': 'T', 'x1': 45, 'y1': 133, 'x2': 103, 'y2': 138, 'font': 'Arial', 'size': 12.0, 'bold': 0, 'italic': 0, 'underline': 0, 'foreground': 0, 'background': 0xFFFFFF, 'align': 'L', 'text': '', 'priority': 2, },
    {'name': '1_row7', 'type': 'T', 'x1': 45, 'y1': 138, 'x2': 103, 'y2': 143, 'font': 'Arial', 'size': 12.0, 'bold': 0, 'italic': 0, 'underline': 0, 'foreground': 0, 'background': 0xFFFFFF, 'align': 'L', 'text': '', 'priority': 2, },
    {'name': '1_row8', 'type': 'T', 'x1': 45, 'y1': 143, 'x2': 103, 'y2': 148, 'font': 'Arial', 'size': 12.0, 'bold': 0, 'italic': 0, 'underline': 0, 'foreground': 0, 'background': 0xFFFFFF, 'align': 'L', 'text': '', 'priority': 2, },
    {'name': '1_row9', 'type': 'T', 'x1': 45, 'y1': 148, 'x2': 103, 'y2': 153, 'font': 'Arial', 'size': 12.0, 'bold': 0, 'italic': 0, 'underline': 0, 'foreground': 0, 'background': 0xFFFFFF, 'align': 'L', 'text': '', 'priority': 2, },

    {'name': '2_qrcode', 'type': 'I', 'x1': 7, 'y1': 168, 'x2': 47, 'y2': 208, 'font': None, 'size': 0.0, 'bold': 0, 'italic': 0, 'underline': 0, 'foreground': 0, 'background': 0xFFFFFF, 'align': 'L', 'text': '', 'priority': 2, },
    {'name': '2_id', 'type': 'T', 'x1': 7, 'y1': 208, 'x2': 47, 'y2': 211, 'font': 'Arial', 'size': 20.0, 'bold': 1, 'italic': 0, 'underline': 0, 'foreground': 0, 'background': 0xFFFFFF, 'align': 'C', 'text': '', 'priority': 2, },
    {'name': '2_row1', 'type': 'T', 'x1': 45, 'y1': 168, 'x2': 103, 'y2': 183, 'font': 'Arial', 'size': 18.0, 'bold': 1, 'italic': 0, 'underline': 0, 'foreground': 0, 'background': 0xFFFFFF, 'align': 'L', 'text': '', 'priority': 2, },
    {'name': '2_row2', 'type': 'T', 'x1': 45, 'y1': 183, 'x2': 103, 'y2': 188, 'font': 'Arial', 'size': 18.0, 'bold': 1, 'italic': 0, 'underline': 0, 'foreground': 0, 'background': 0xFFFFFF, 'align': 'L', 'text': '', 'priority': 2, },
    {'name': '2_row3', 'type': 'T', 'x1': 45, 'y1': 193, 'x2': 103, 'y2': 198, 'font': 'Arial', 'size': 12.0, 'bold': 0, 'italic': 0, 'underline': 0, 'foreground': 0, 'background': 0xFFFFFF, 'align': 'L', 'text': '', 'priority': 2, },
    {'name': '2_row4', 'type': 'T', 'x1': 45, 'y1': 198, 'x2': 103, 'y2': 203, 'font': 'Arial', 'size': 12.0, 'bold': 0, 'italic': 0, 'underline': 0, 'foreground': 0, 'background': 0xFFFFFF, 'align': 'L', 'text': '', 'priority': 2, },
    {'name': '2_row5', 'type': 'T', 'x1': 45, 'y1': 203, 'x2': 103, 'y2': 208, 'font': 'Arial', 'size': 12.0, 'bold': 0, 'italic': 0, 'underline': 0, 'foreground': 0, 'background': 0xFFFFFF, 'align': 'L', 'text': '', 'priority': 2, },
    {'name': '2_row6', 'type': 'T', 'x1': 45, 'y1': 208, 'x2': 103, 'y2': 213, 'font': 'Arial', 'size': 12.0, 'bold': 0, 'italic': 0, 'underline': 0, 'foreground': 0, 'background': 0xFFFFFF, 'align': 'L', 'text': '', 'priority': 2, },
    {'name': '2_row7', 'type': 'T', 'x1': 45, 'y1': 213, 'x2': 103, 'y2': 218, 'font': 'Arial', 'size': 12.0, 'bold': 0, 'italic': 0, 'underline': 0, 'foreground': 0, 'background': 0xFFFFFF, 'align': 'L', 'text': '', 'priority': 2, },
    {'name': '2_row8', 'type': 'T', 'x1': 45, 'y1': 218, 'x2': 103, 'y2': 223, 'font': 'Arial', 'size': 12.0, 'bold': 0, 'italic': 0, 'underline': 0, 'foreground': 0, 'background': 0xFFFFFF, 'align': 'L', 'text': '', 'priority': 2, },
    {'name': '2_row9', 'type': 'T', 'x1': 45, 'y1': 223, 'x2': 103, 'y2': 228, 'font': 'Arial', 'size': 12.0, 'bold': 0, 'italic': 0, 'underline': 0, 'foreground': 0, 'background': 0xFFFFFF, 'align': 'L', 'text': '', 'priority': 2, },

    # left is 117
    {'name': '3_qrcode', 'type': 'I', 'x1': 110, 'y1': 15, 'x2': 150, 'y2': 55, 'font': None, 'size': 0.0, 'bold': 0, 'italic': 0, 'underline': 0, 'foreground': 0, 'background': 0xFFFFFF, 'align': 'L', 'text': '', 'priority': 2, },
    {'name': '3_id', 'type': 'T', 'x1': 110, 'y1': 55, 'x2': 150, 'y2': 58, 'font': 'Arial', 'size': 20.0, 'bold': 1, 'italic': 0, 'underline': 0, 'foreground': 0, 'background': 0xFFFFFF, 'align': 'C', 'text': '', 'priority': 2, },
    {'name': '3_row1', 'type': 'T', 'x1': 148, 'y1': 15, 'x2': 211, 'y2': 30, 'font': 'Arial', 'size': 18.0, 'bold': 1, 'italic': 0, 'underline': 0, 'foreground': 0, 'background': 0xFFFFFF, 'align': 'L', 'text': '', 'priority': 2, },
    {'name': '3_row2', 'type': 'T', 'x1': 148, 'y1': 30, 'x2': 211, 'y2': 35, 'font': 'Arial', 'size': 18.0, 'bold': 1, 'italic': 0, 'underline': 0, 'foreground': 0, 'background': 0xFFFFFF, 'align': 'L', 'text': '', 'priority': 2, },
    {'name': '3_row3', 'type': 'T', 'x1': 148, 'y1': 40, 'x2': 211, 'y2': 45, 'font': 'Arial', 'size': 12.0, 'bold': 0, 'italic': 0, 'underline': 0, 'foreground': 0, 'background': 0xFFFFFF, 'align': 'L', 'text': '', 'priority': 2, },
    {'name': '3_row4', 'type': 'T', 'x1': 148, 'y1': 45, 'x2': 211, 'y2': 50, 'font': 'Arial', 'size': 12.0, 'bold': 0, 'italic': 0, 'underline': 0, 'foreground': 0, 'background': 0xFFFFFF, 'align': 'L', 'text': '', 'priority': 2, },
    {'name': '3_row5', 'type': 'T', 'x1': 148, 'y1': 50, 'x2': 211, 'y2': 55, 'font': 'Arial', 'size': 12.0, 'bold': 0, 'italic': 0, 'underline': 0, 'foreground': 0, 'background': 0xFFFFFF, 'align': 'L', 'text': '', 'priority': 2, },
    {'name': '3_row6', 'type': 'T', 'x1': 148, 'y1': 55, 'x2': 211, 'y2': 60, 'font': 'Arial', 'size': 12.0, 'bold': 0, 'italic': 0, 'underline': 0, 'foreground': 0, 'background': 0xFFFFFF, 'align': 'L', 'text': '', 'priority': 2, },
    {'name': '3_row7', 'type': 'T', 'x1': 148, 'y1': 60, 'x2': 211, 'y2': 65, 'font': 'Arial', 'size': 12.0, 'bold': 0, 'italic': 0, 'underline': 0, 'foreground': 0, 'background': 0xFFFFFF, 'align': 'L', 'text': '', 'priority': 2, },
    {'name': '3_row8', 'type': 'T', 'x1': 148, 'y1': 65, 'x2': 211, 'y2': 70, 'font': 'Arial', 'size': 12.0, 'bold': 0, 'italic': 0, 'underline': 0, 'foreground': 0, 'background': 0xFFFFFF, 'align': 'L', 'text': '', 'priority': 2, },
    {'name': '3_row9', 'type': 'T', 'x1': 148, 'y1': 70, 'x2': 211, 'y2': 75, 'font': 'Arial', 'size': 12.0, 'bold': 0, 'italic': 0, 'underline': 0, 'foreground': 0, 'background': 0xFFFFFF, 'align': 'L', 'text': '', 'priority': 2, },

    {'name': '4_qrcode', 'type': 'I', 'x1': 110, 'y1': 93, 'x2': 150, 'y2': 133, 'font': None, 'size': 0.0, 'bold': 0, 'italic': 0, 'underline': 0, 'foreground': 0, 'background': 0xFFFFFF, 'align': 'L', 'text': '', 'priority': 2, },
    {'name': '4_id', 'type': 'T', 'x1': 110, 'y1': 133, 'x2': 150, 'y2': 136, 'font': 'Arial', 'size': 20.0, 'bold': 1, 'italic': 0, 'underline': 0, 'foreground': 0, 'background': 0xFFFFFF, 'align': 'C', 'text': '', 'priority': 2, },
    {'name': '4_row1', 'type': 'T', 'x1': 148, 'y1': 93, 'x2': 211, 'y2': 108, 'font': 'Arial', 'size': 18.0, 'bold': 1, 'italic': 0, 'underline': 0, 'foreground': 0, 'background': 0xFFFFFF, 'align': 'L', 'text': '', 'priority': 2, },
    {'name': '4_row2', 'type': 'T', 'x1': 148, 'y1': 108, 'x2': 211, 'y2': 113, 'font': 'Arial', 'size': 18.0, 'bold': 1, 'italic': 0, 'underline': 0, 'foreground': 0, 'background': 0xFFFFFF, 'align': 'L', 'text': '', 'priority': 2, },
    {'name': '4_row3', 'type': 'T', 'x1': 148, 'y1': 118, 'x2': 211, 'y2': 123, 'font': 'Arial', 'size': 12.0, 'bold': 0, 'italic': 0, 'underline': 0, 'foreground': 0, 'background': 0xFFFFFF, 'align': 'L', 'text': '', 'priority': 2, },
    {'name': '4_row4', 'type': 'T', 'x1': 148, 'y1': 123, 'x2': 211, 'y2': 128, 'font': 'Arial', 'size': 12.0, 'bold': 0, 'italic': 0, 'underline': 0, 'foreground': 0, 'background': 0xFFFFFF, 'align': 'L', 'text': '', 'priority': 2, },
    {'name': '4_row5', 'type': 'T', 'x1': 148, 'y1': 128, 'x2': 211, 'y2': 133, 'font': 'Arial', 'size': 12.0, 'bold': 0, 'italic': 0, 'underline': 0, 'foreground': 0, 'background': 0xFFFFFF, 'align': 'L', 'text': '', 'priority': 2, },
    {'name': '4_row6', 'type': 'T', 'x1': 148, 'y1': 133, 'x2': 211, 'y2': 138, 'font': 'Arial', 'size': 12.0, 'bold': 0, 'italic': 0, 'underline': 0, 'foreground': 0, 'background': 0xFFFFFF, 'align': 'L', 'text': '', 'priority': 2, },
    {'name': '4_row7', 'type': 'T', 'x1': 148, 'y1': 138, 'x2': 211, 'y2': 143, 'font': 'Arial', 'size': 12.0, 'bold': 0, 'italic': 0, 'underline': 0, 'foreground': 0, 'background': 0xFFFFFF, 'align': 'L', 'text': '', 'priority': 2, },
    {'name': '4_row8', 'type': 'T', 'x1': 148, 'y1': 143, 'x2': 211, 'y2': 148, 'font': 'Arial', 'size': 12.0, 'bold': 0, 'italic': 0, 'underline': 0, 'foreground': 0, 'background': 0xFFFFFF, 'align': 'L', 'text': '', 'priority': 2, },
    {'name': '4_row9', 'type': 'T', 'x1': 148, 'y1': 148, 'x2': 211, 'y2': 153, 'font': 'Arial', 'size': 12.0, 'bold': 0, 'italic': 0, 'underline': 0, 'foreground': 0, 'background': 0xFFFFFF, 'align': 'L', 'text': '', 'priority': 2, },

    {'name': '5_qrcode', 'type': 'I', 'x1': 110, 'y1': 168, 'x2': 150, 'y2': 208, 'font': None, 'size': 0.0, 'bold': 0, 'italic': 0, 'underline': 0, 'foreground': 0, 'background': 0xFFFFFF, 'align': 'L', 'text': '', 'priority': 2, },
    {'name': '5_id', 'type': 'T', 'x1': 110, 'y1': 208, 'x2': 150, 'y2': 211, 'font': 'Arial', 'size': 20.0, 'bold': 1, 'italic': 0, 'underline': 0, 'foreground': 0, 'background': 0xFFFFFF, 'align': 'C', 'text': '', 'priority': 2, },
    {'name': '5_row1', 'type': 'T', 'x1': 148, 'y1': 168, 'x2': 211, 'y2': 183, 'font': 'Arial', 'size': 18.0, 'bold': 1, 'italic': 0, 'underline': 0, 'foreground': 0, 'background': 0xFFFFFF, 'align': 'L', 'text': '', 'priority': 2, },
    {'name': '5_row2', 'type': 'T', 'x1': 148, 'y1': 183, 'x2': 211, 'y2': 188, 'font': 'Arial', 'size': 18.0, 'bold': 1, 'italic': 0, 'underline': 0, 'foreground': 0, 'background': 0xFFFFFF, 'align': 'L', 'text': '', 'priority': 2, },
    {'name': '5_row3', 'type': 'T', 'x1': 148, 'y1': 193, 'x2': 211, 'y2': 198, 'font': 'Arial', 'size': 12.0, 'bold': 0, 'italic': 0, 'underline': 0, 'foreground': 0, 'background': 0xFFFFFF, 'align': 'L', 'text': '', 'priority': 2, },
    {'name': '5_row4', 'type': 'T', 'x1': 148, 'y1': 198, 'x2': 211, 'y2': 203, 'font': 'Arial', 'size': 12.0, 'bold': 0, 'italic': 0, 'underline': 0, 'foreground': 0, 'background': 0xFFFFFF, 'align': 'L', 'text': '', 'priority': 2, },
    {'name': '5_row5', 'type': 'T', 'x1': 148, 'y1': 203, 'x2': 211, 'y2': 208, 'font': 'Arial', 'size': 12.0, 'bold': 0, 'italic': 0, 'underline': 0, 'foreground': 0, 'background': 0xFFFFFF, 'align': 'L', 'text': '', 'priority': 2, },
    {'name': '5_row6', 'type': 'T', 'x1': 148, 'y1': 208, 'x2': 211, 'y2': 213, 'font': 'Arial', 'size': 12.0, 'bold': 0, 'italic': 0, 'underline': 0, 'foreground': 0, 'background': 0xFFFFFF, 'align': 'L', 'text': '', 'priority': 2, },
    {'name': '5_row7', 'type': 'T', 'x1': 148, 'y1': 213, 'x2': 211, 'y2': 218, 'font': 'Arial', 'size': 12.0, 'bold': 0, 'italic': 0, 'underline': 0, 'foreground': 0, 'background': 0xFFFFFF, 'align': 'L', 'text': '', 'priority': 2, },
    {'name': '5_row8', 'type': 'T', 'x1': 148, 'y1': 218, 'x2': 211, 'y2': 223, 'font': 'Arial', 'size': 12.0, 'bold': 0, 'italic': 0, 'underline': 0, 'foreground': 0, 'background': 0xFFFFFF, 'align': 'L', 'text': '', 'priority': 2, },
    {'name': '5_row9', 'type': 'T', 'x1': 148, 'y1': 223, 'x2': 211, 'y2': 228, 'font': 'Arial', 'size': 12.0, 'bold': 0, 'italic': 0, 'underline': 0, 'foreground': 0, 'background': 0xFFFFFF, 'align': 'L', 'text': '', 'priority': 2, },

]


#this will define the elements that will compose the multitemplate for the small labels
#note it is required that small matches the name of the samplelabelsize in the database.
multismall = [
    # top margin: 12.7
    # left 3.175
    # right margin 4.7625
    # bottom margin 12.7
    # center gutter 4.7625
    {'name': '0_qrcode', 'type': 'I', 'x1': 7, 'y1': 15, 'x2': 47, 'y2': 55, 'font': None, 'size': 0.0, 'bold': 0, 'italic': 0, 'underline': 0, 'foreground': 0, 'background': 0xFFFFFF, 'align': 'L', 'text': '', 'priority': 2, },
    {'name': '0_id', 'type': 'T', 'x1': 7, 'y1': 55, 'x2': 47, 'y2': 58, 'font': 'Arial', 'size': 20.0, 'bold': 1, 'italic': 0, 'underline': 0, 'foreground': 0, 'background': 0xFFFFFF, 'align': 'C', 'text': '', 'priority': 2, },
    {'name': '0_row1', 'type': 'T', 'x1': 45, 'y1': 15, 'x2': 108, 'y2': 30, 'font': 'Arial', 'size': 18.0, 'bold': 1, 'italic': 0, 'underline': 0, 'foreground': 0, 'background': 0xFFFFFF, 'align': 'L', 'text': '', 'priority': 2, },
    {'name': '0_row2', 'type': 'T', 'x1': 45, 'y1': 29, 'x2': 108, 'y2': 34, 'font': 'Arial', 'size': 12.0, 'bold': 0, 'italic': 0, 'underline': 0, 'foreground': 0, 'background': 0xFFFFFF, 'align': 'L', 'text': '', 'priority': 2, },
    {'name': '0_row3', 'type': 'T', 'x1': 45, 'y1': 34, 'x2': 108, 'y2': 39, 'font': 'Arial', 'size': 12.0, 'bold': 0, 'italic': 0, 'underline': 0, 'foreground': 0, 'background': 0xFFFFFF, 'align': 'L', 'text': '', 'priority': 2, },
    {'name': '0_row4', 'type': 'T', 'x1': 45, 'y1': 39, 'x2': 108, 'y2': 44, 'font': 'Arial', 'size': 12.0, 'bold': 0, 'italic': 0, 'underline': 0, 'foreground': 0, 'background': 0xFFFFFF, 'align': 'L', 'text': '', 'priority': 2, },

    {'name': '1_qrcode', 'type': 'I', 'x1': 7, 'y1': 66, 'x2': 47, 'y2': 106, 'font': None, 'size': 0.0, 'bold': 0, 'italic': 0, 'underline': 0, 'foreground': 0, 'background': 0xFFFFFF, 'align': 'L', 'text': '', 'priority': 2, },
    {'name': '1_id', 'type': 'T', 'x1': 7, 'y1': 106, 'x2': 47, 'y2': 109, 'font': 'Arial', 'size': 20.0, 'bold': 1, 'italic': 0, 'underline': 0, 'foreground': 0, 'background': 0xFFFFFF, 'align': 'C', 'text': '', 'priority': 2, },
    {'name': '1_row1', 'type': 'T', 'x1': 45, 'y1': 66, 'x2': 108, 'y2': 81, 'font': 'Arial', 'size': 18.0, 'bold': 1, 'italic': 0, 'underline': 0, 'foreground': 0, 'background': 0xFFFFFF, 'align': 'L', 'text': '', 'priority': 2, },
    {'name': '1_row2', 'type': 'T', 'x1': 45, 'y1': 80, 'x2': 108, 'y2': 85, 'font': 'Arial', 'size': 12.0, 'bold': 0, 'italic': 0, 'underline': 0, 'foreground': 0, 'background': 0xFFFFFF, 'align': 'L', 'text': '', 'priority': 2, },
    {'name': '1_row3', 'type': 'T', 'x1': 45, 'y1': 85, 'x2': 108, 'y2': 90, 'font': 'Arial', 'size': 12.0, 'bold': 0, 'italic': 0, 'underline': 0, 'foreground': 0, 'background': 0xFFFFFF, 'align': 'L', 'text': '', 'priority': 2, },
    {'name': '1_row4', 'type': 'T', 'x1': 45, 'y1': 90, 'x2': 108, 'y2': 95, 'font': 'Arial', 'size': 12.0, 'bold': 0, 'italic': 0, 'underline': 0, 'foreground': 0, 'background': 0xFFFFFF, 'align': 'L', 'text': '', 'priority': 2, },

    {'name': '2_qrcode', 'type': 'I', 'x1': 7, 'y1': 117, 'x2': 47, 'y2': 157, 'font': None, 'size': 0.0, 'bold': 0, 'italic': 0, 'underline': 0, 'foreground': 0, 'background': 0xFFFFFF, 'align': 'L', 'text': '', 'priority': 2, },
    {'name': '2_id', 'type': 'T', 'x1': 7, 'y1': 157, 'x2': 47, 'y2': 160, 'font': 'Arial', 'size': 20.0, 'bold': 1, 'italic': 0, 'underline': 0, 'foreground': 0, 'background': 0xFFFFFF, 'align': 'C', 'text': '', 'priority': 2, },
    {'name': '2_row1', 'type': 'T', 'x1': 45, 'y1': 117, 'x2': 108, 'y2': 132, 'font': 'Arial', 'size': 18.0, 'bold': 1, 'italic': 0, 'underline': 0, 'foreground': 0, 'background': 0xFFFFFF, 'align': 'L', 'text': '', 'priority': 2, },
    {'name': '2_row2', 'type': 'T', 'x1': 45, 'y1': 131, 'x2': 108, 'y2': 136, 'font': 'Arial', 'size': 12.0, 'bold': 0, 'italic': 0, 'underline': 0, 'foreground': 0, 'background': 0xFFFFFF, 'align': 'L', 'text': '', 'priority': 2, },
    {'name': '2_row3', 'type': 'T', 'x1': 45, 'y1': 136, 'x2': 108, 'y2': 141, 'font': 'Arial', 'size': 12.0, 'bold': 0, 'italic': 0, 'underline': 0, 'foreground': 0, 'background': 0xFFFFFF, 'align': 'L', 'text': '', 'priority': 2, },
    {'name': '2_row4', 'type': 'T', 'x1': 45, 'y1': 141, 'x2': 108, 'y2': 146, 'font': 'Arial', 'size': 12.0, 'bold': 0, 'italic': 0, 'underline': 0, 'foreground': 0, 'background': 0xFFFFFF, 'align': 'L', 'text': '', 'priority': 2, },

    {'name': '3_qrcode', 'type': 'I', 'x1': 7, 'y1': 168, 'x2': 47, 'y2': 208, 'font': None, 'size': 0.0, 'bold': 0, 'italic': 0, 'underline': 0, 'foreground': 0, 'background': 0xFFFFFF, 'align': 'L', 'text': '', 'priority': 2, },
    {'name': '3_id', 'type': 'T', 'x1': 7, 'y1': 208, 'x2': 47, 'y2': 211, 'font': 'Arial', 'size': 20.0, 'bold': 1, 'italic': 0, 'underline': 0, 'foreground': 0, 'background': 0xFFFFFF, 'align': 'C', 'text': '', 'priority': 2, },
    {'name': '3_row1', 'type': 'T', 'x1': 45, 'y1': 168, 'x2': 108, 'y2': 183, 'font': 'Arial', 'size': 18.0, 'bold': 1, 'italic': 0, 'underline': 0, 'foreground': 0, 'background': 0xFFFFFF, 'align': 'L', 'text': '', 'priority': 2, },
    {'name': '3_row2', 'type': 'T', 'x1': 45, 'y1': 182, 'x2': 108, 'y2': 187, 'font': 'Arial', 'size': 12.0, 'bold': 0, 'italic': 0, 'underline': 0, 'foreground': 0, 'background': 0xFFFFFF, 'align': 'L', 'text': '', 'priority': 2, },
    {'name': '3_row3', 'type': 'T', 'x1': 45, 'y1': 187, 'x2': 108, 'y2': 192, 'font': 'Arial', 'size': 12.0, 'bold': 0, 'italic': 0, 'underline': 0, 'foreground': 0, 'background': 0xFFFFFF, 'align': 'L', 'text': '', 'priority': 2, },
    {'name': '3_row4', 'type': 'T', 'x1': 45, 'y1': 192, 'x2': 108, 'y2': 197, 'font': 'Arial', 'size': 12.0, 'bold': 0, 'italic': 0, 'underline': 0, 'foreground': 0, 'background': 0xFFFFFF, 'align': 'L', 'text': '', 'priority': 2, },

    {'name': '4_qrcode', 'type': 'I', 'x1': 7, 'y1': 219, 'x2': 47, 'y2': 259, 'font': None, 'size': 0.0, 'bold': 0, 'italic': 0, 'underline': 0, 'foreground': 0, 'background': 0xFFFFFF, 'align': 'L', 'text': '', 'priority': 2, },
    {'name': '4_id', 'type': 'T', 'x1': 7, 'y1': 259, 'x2': 47, 'y2': 262, 'font': 'Arial', 'size': 20.0, 'bold': 1, 'italic': 0, 'underline': 0, 'foreground': 0, 'background': 0xFFFFFF, 'align': 'C', 'text': '', 'priority': 2, },
    {'name': '4_row1', 'type': 'T', 'x1': 45, 'y1': 219, 'x2': 108, 'y2': 234, 'font': 'Arial', 'size': 18.0, 'bold': 1, 'italic': 0, 'underline': 0, 'foreground': 0, 'background': 0xFFFFFF, 'align': 'L', 'text': '', 'priority': 2, },
    {'name': '4_row2', 'type': 'T', 'x1': 45, 'y1': 233, 'x2': 108, 'y2': 238, 'font': 'Arial', 'size': 12.0, 'bold': 0, 'italic': 0, 'underline': 0, 'foreground': 0, 'background': 0xFFFFFF, 'align': 'L', 'text': '', 'priority': 2, },
    {'name': '4_row3', 'type': 'T', 'x1': 45, 'y1': 238, 'x2': 108, 'y2': 243, 'font': 'Arial', 'size': 12.0, 'bold': 0, 'italic': 0, 'underline': 0, 'foreground': 0, 'background': 0xFFFFFF, 'align': 'L', 'text': '', 'priority': 2, },
    {'name': '4_row4', 'type': 'T', 'x1': 45, 'y1': 243, 'x2': 108, 'y2': 248, 'font': 'Arial', 'size': 12.0, 'bold': 0, 'italic': 0, 'underline': 0, 'foreground': 0, 'background': 0xFFFFFF, 'align': 'L', 'text': '', 'priority': 2, },

    # left is 110
    {'name': '5_qrcode', 'type': 'I', 'x1': 117, 'y1': 15, 'x2': 157, 'y2': 55, 'font': None, 'size': 0.0, 'bold': 0, 'italic': 0, 'underline': 0, 'foreground': 0, 'background': 0xFFFFFF, 'align': 'L', 'text': '', 'priority': 2, },
    {'name': '5_id', 'type': 'T', 'x1': 117, 'y1': 55, 'x2': 157, 'y2': 58, 'font': 'Arial', 'size': 20.0, 'bold': 1, 'italic': 0, 'underline': 0, 'foreground': 0, 'background': 0xFFFFFF, 'align': 'C', 'text': '', 'priority': 2, },
    {'name': '5_row1', 'type': 'T', 'x1': 155, 'y1': 15, 'x2': 218, 'y2': 30, 'font': 'Arial', 'size': 18.0, 'bold': 1, 'italic': 0, 'underline': 0, 'foreground': 0, 'background': 0xFFFFFF, 'align': 'L', 'text': '', 'priority': 2, },
    {'name': '5_row2', 'type': 'T', 'x1': 155, 'y1': 29, 'x2': 218, 'y2': 34, 'font': 'Arial', 'size': 12.0, 'bold': 0, 'italic': 0, 'underline': 0, 'foreground': 0, 'background': 0xFFFFFF, 'align': 'L', 'text': '', 'priority': 2, },
    {'name': '5_row3', 'type': 'T', 'x1': 155, 'y1': 34, 'x2': 218, 'y2': 39, 'font': 'Arial', 'size': 12.0, 'bold': 0, 'italic': 0, 'underline': 0, 'foreground': 0, 'background': 0xFFFFFF, 'align': 'L', 'text': '', 'priority': 2, },
    {'name': '5_row4', 'type': 'T', 'x1': 155, 'y1': 39, 'x2': 218, 'y2': 44, 'font': 'Arial', 'size': 12.0, 'bold': 0, 'italic': 0, 'underline': 0, 'foreground': 0, 'background': 0xFFFFFF, 'align': 'L', 'text': '', 'priority': 2, },

    {'name': '6_qrcode', 'type': 'I', 'x1': 117, 'y1': 66, 'x2': 157, 'y2': 106, 'font': None, 'size': 0.0, 'bold': 0, 'italic': 0, 'underline': 0, 'foreground': 0, 'background': 0xFFFFFF, 'align': 'L', 'text': '', 'priority': 2, },
    {'name': '6_id', 'type': 'T', 'x1': 117, 'y1': 106, 'x2': 157, 'y2': 109, 'font': 'Arial', 'size': 20.0, 'bold': 1, 'italic': 0, 'underline': 0, 'foreground': 0, 'background': 0xFFFFFF, 'align': 'C', 'text': '', 'priority': 2, },
    {'name': '6_row1', 'type': 'T', 'x1': 155, 'y1': 66, 'x2': 218, 'y2': 81, 'font': 'Arial', 'size': 18.0, 'bold': 1, 'italic': 0, 'underline': 0, 'foreground': 0, 'background': 0xFFFFFF, 'align': 'L', 'text': '', 'priority': 2, },
    {'name': '6_row2', 'type': 'T', 'x1': 155, 'y1': 80, 'x2': 218, 'y2': 85, 'font': 'Arial', 'size': 12.0, 'bold': 0, 'italic': 0, 'underline': 0, 'foreground': 0, 'background': 0xFFFFFF, 'align': 'L', 'text': '', 'priority': 2, },
    {'name': '6_row3', 'type': 'T', 'x1': 155, 'y1': 85, 'x2': 218, 'y2': 90, 'font': 'Arial', 'size': 12.0, 'bold': 0, 'italic': 0, 'underline': 0, 'foreground': 0, 'background': 0xFFFFFF, 'align': 'L', 'text': '', 'priority': 2, },
    {'name': '6_row4', 'type': 'T', 'x1': 155, 'y1': 90, 'x2': 218, 'y2': 95, 'font': 'Arial', 'size': 12.0, 'bold': 0, 'italic': 0, 'underline': 0, 'foreground': 0, 'background': 0xFFFFFF, 'align': 'L', 'text': '', 'priority': 2, },

    {'name': '7_qrcode', 'type': 'I', 'x1': 117, 'y1': 117, 'x2': 157, 'y2': 157, 'font': None, 'size': 0.0, 'bold': 0, 'italic': 0, 'underline': 0, 'foreground': 0, 'background': 0xFFFFFF, 'align': 'L', 'text': '', 'priority': 2, },
    {'name': '7_id', 'type': 'T', 'x1': 117, 'y1': 157, 'x2': 157, 'y2': 160, 'font': 'Arial', 'size': 20.0, 'bold': 1, 'italic': 0, 'underline': 0, 'foreground': 0, 'background': 0xFFFFFF, 'align': 'C', 'text': '', 'priority': 2, },
    {'name': '7_row1', 'type': 'T', 'x1': 155, 'y1': 117, 'x2': 218, 'y2': 132, 'font': 'Arial', 'size': 18.0, 'bold': 1, 'italic': 0, 'underline': 0, 'foreground': 0, 'background': 0xFFFFFF, 'align': 'L', 'text': '', 'priority': 2, },
    {'name': '7_row2', 'type': 'T', 'x1': 155, 'y1': 131, 'x2': 218, 'y2': 136, 'font': 'Arial', 'size': 12.0, 'bold': 0, 'italic': 0, 'underline': 0, 'foreground': 0, 'background': 0xFFFFFF, 'align': 'L', 'text': '', 'priority': 2, },
    {'name': '7_row3', 'type': 'T', 'x1': 155, 'y1': 136, 'x2': 218, 'y2': 141, 'font': 'Arial', 'size': 12.0, 'bold': 0, 'italic': 0, 'underline': 0, 'foreground': 0, 'background': 0xFFFFFF, 'align': 'L', 'text': '', 'priority': 2, },
    {'name': '7_row4', 'type': 'T', 'x1': 155, 'y1': 141, 'x2': 218, 'y2': 146, 'font': 'Arial', 'size': 12.0, 'bold': 0, 'italic': 0, 'underline': 0, 'foreground': 0, 'background': 0xFFFFFF, 'align': 'L', 'text': '', 'priority': 2, },

    {'name': '8_qrcode', 'type': 'I', 'x1': 117, 'y1': 168, 'x2': 157, 'y2': 208, 'font': None, 'size': 0.0, 'bold': 0, 'italic': 0, 'underline': 0, 'foreground': 0, 'background': 0xFFFFFF, 'align': 'L', 'text': '', 'priority': 2, },
    {'name': '8_id', 'type': 'T', 'x1': 117, 'y1': 208, 'x2': 157, 'y2': 211, 'font': 'Arial', 'size': 20.0, 'bold': 1, 'italic': 0, 'underline': 0, 'foreground': 0, 'background': 0xFFFFFF, 'align': 'C', 'text': '', 'priority': 2, },
    {'name': '8_row1', 'type': 'T', 'x1': 155, 'y1': 168, 'x2': 218, 'y2': 183, 'font': 'Arial', 'size': 18.0, 'bold': 1, 'italic': 0, 'underline': 0, 'foreground': 0, 'background': 0xFFFFFF, 'align': 'L', 'text': '', 'priority': 2, },
    {'name': '8_row2', 'type': 'T', 'x1': 155, 'y1': 182, 'x2': 218, 'y2': 187, 'font': 'Arial', 'size': 12.0, 'bold': 0, 'italic': 0, 'underline': 0, 'foreground': 0, 'background': 0xFFFFFF, 'align': 'L', 'text': '', 'priority': 2, },
    {'name': '8_row3', 'type': 'T', 'x1': 155, 'y1': 187, 'x2': 218, 'y2': 192, 'font': 'Arial', 'size': 12.0, 'bold': 0, 'italic': 0, 'underline': 0, 'foreground': 0, 'background': 0xFFFFFF, 'align': 'L', 'text': '', 'priority': 2, },
    {'name': '8_row4', 'type': 'T', 'x1': 155, 'y1': 192, 'x2': 218, 'y2': 197, 'font': 'Arial', 'size': 12.0, 'bold': 0, 'italic': 0, 'underline': 0, 'foreground': 0, 'background': 0xFFFFFF, 'align': 'L', 'text': '', 'priority': 2, },

    {'name': '9_qrcode', 'type': 'I', 'x1': 117, 'y1': 219, 'x2': 157, 'y2': 259, 'font': None, 'size': 0.0, 'bold': 0, 'italic': 0, 'underline': 0, 'foreground': 0, 'background': 0xFFFFFF, 'align': 'L', 'text': '', 'priority': 2, },
    {'name': '9_id', 'type': 'T', 'x1': 117, 'y1': 259, 'x2': 157, 'y2': 262, 'font': 'Arial', 'size': 20.0, 'bold': 1, 'italic': 0, 'underline': 0, 'foreground': 0, 'background': 0xFFFFFF, 'align': 'C', 'text': '', 'priority': 2, },
    {'name': '9_row1', 'type': 'T', 'x1': 155, 'y1': 219, 'x2': 218, 'y2': 234, 'font': 'Arial', 'size': 18.0, 'bold': 1, 'italic': 0, 'underline': 0, 'foreground': 0, 'background': 0xFFFFFF, 'align': 'L', 'text': '', 'priority': 2, },
    {'name': '9_row2', 'type': 'T', 'x1': 155, 'y1': 233, 'x2': 218, 'y2': 238, 'font': 'Arial', 'size': 12.0, 'bold': 0, 'italic': 0, 'underline': 0, 'foreground': 0, 'background': 0xFFFFFF, 'align': 'L', 'text': '', 'priority': 2, },
    {'name': '9_row3', 'type': 'T', 'x1': 155, 'y1': 238, 'x2': 218, 'y2': 243, 'font': 'Arial', 'size': 12.0, 'bold': 0, 'italic': 0, 'underline': 0, 'foreground': 0, 'background': 0xFFFFFF, 'align': 'L', 'text': '', 'priority': 2, },
    {'name': '9_row4', 'type': 'T', 'x1': 155, 'y1': 243, 'x2': 218, 'y2': 248, 'font': 'Arial', 'size': 12.0, 'bold': 0, 'italic': 0, 'underline': 0, 'foreground': 0, 'background': 0xFFFFFF, 'align': 'L', 'text': '', 'priority': 2, },

]
