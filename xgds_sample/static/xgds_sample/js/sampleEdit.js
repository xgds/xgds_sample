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

var xgds_sample = xgds_sample || {};
$.extend(xgds_sample,{
	initializeSampleEditForm: function(){
		$('#id_resource').parent().parent().hide();
		$('#id_latitude').parent().parent().hide();
		$('#id_longitude').parent().parent().hide();
		$('#id_altitude').parent().parent().hide();
		$('#id_flight').parent().parent().hide();
		this.setupCollectorInput();
	},
	toggleAdvancedInput: function() {
		$('#id_resource').parent().parent().toggle();
		$('#id_latitude').parent().parent().toggle();
		$('#id_longitude').parent().parent().toggle();
		$('#id_altitude').parent().parent().toggle();
		$('#id_flight').parent().parent().toggle();
		if ($('#id_resource').is(":visible")) {
			$('.toggleInputFields').html('Close out-of-sim fields');	
		} else {
			$('.toggleInputFields').html('Open out-of-sim fields');	
		}
	},
	setupCollectorInput: function() {
		// typeahead autocomplete for input fields

		var substringMatcher = function(strs) {
			  return function findMatches(q, cb) {
			    var matches, substringRegex;

			    // an array that will be populated with substring matches
			    matches = [];

			    // regex used to determine if a string contains the substring `q`
			    substrRegex = new RegExp(q, 'i');

			    // iterate through the pool of strings and for any string that
			    // contains the substring `q`, add it to the `matches` array
			    $.each(strs, function(i, str) {
			      if (substrRegex.test(str)) {
			        matches.push(str);
			      }
			    });

			    cb(matches);
			  };
			};

			
		$('#id_collector').typeahead({
			  hint: true,
			  highlight: true,
			  minLength: 1
			},
			{
			  name: 'collector',
			  source: substringMatcher(collectors)
			});
	}

});
