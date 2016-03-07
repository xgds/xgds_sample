//__BEGIN_LICENSE__
// Copyright (c) 2015, United States Government, as represented by the
// Administrator of the National Aeronautics and Space Administration.
// All rights reserved.
//
// The xGDS platform is licensed under the Apache License, Version 2.0
// (the "License"); you may not use this file except in compliance with the License.
// You may obtain a copy of the License at
// http://www.apache.org/licenses/LICENSE-2.0.
//
// Unless required by applicable law or agreed to in writing, software distributed
// under the License is distributed on an "AS IS" BASIS, WITHOUT WARRANTIES OR
// CONDITIONS OF ANY KIND, either express or implied. See the License for the
// specific language governing permissions and limitations under the License.
//__END_LICENSE__


function setMessage(message){
    $("#message").text(message);
}

function doSimpleSearch(event) {
    var theForm = this.$("#sample_simple_search_form");
    var postData = theForm.serializeArray();
    postData.push({'name':'modelClass', 'value':'xgds_sample.Sample'});
    setMessage("Searching..."); //set message (TODO) 
    event.preventDefault();
    $.ajax({
        url: '/xgds_map_server/doMapSearch',
        dataType: 'json',
        data: postData,
        success: $.proxy(function(data) {
            if (_.isUndefined(data) || data.length === 0){
                setMessage("None found.");
            } else {
            	imageSetsArray = data;
            	theDataTable.fnClearTable();
            	theDataTable.fnAddData(data);
                setMessage("");
                app.vent.trigger("mapSearch:found", data); 
            }
        }, this),
        error: $.proxy(function(data){
            app.vent.trigger("mapSearch:clear");
//            this.searchResultsView.reset();
            setMessage("Search failed.")
        }, this)
      });
}

// datetime picker
var dateTimeOptions = {'controlType': 'select',
	  	       'oneLine': true,
	  	       'showTimezone': false,
	  	       'timezone': '-0000'
	 	       };
$( "#id_form-0-creation_time_lo" ).datetimepicker(dateTimeOptions);
$( "#id_form-0-creation_time_hi" ).datetimepicker(dateTimeOptions);
$( "#id_form-0-modification_time_lo" ).datetimepicker(dateTimeOptions);
$( "#id_form-0-modification_time_hi" ).datetimepicker(dateTimeOptions);