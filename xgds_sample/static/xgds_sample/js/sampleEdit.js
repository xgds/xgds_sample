//__BEGIN_LICENSE__
//Copyright (c) 2015, United States Government, as represented by the
//Administrator of the National Aeronautics and Space Administration.
//All rights reserved.

//The xGDS platform is licensed under the Apache License, Version 2.0
//(the "License"); you may not use this file except in compliance with the License.
//You may obtain a copy of the License at
//http://www.apache.org/licenses/LICENSE-2.0.

//Unless required by applicable law or agreed to in writing, software distributed
//under the License is distributed on an "AS IS" BASIS, WITHOUT WARRANTIES OR
//CONDITIONS OF ANY KIND, either express or implied. See the License for the
//specific language governing permissions and limitations under the License.
//__END_LICENSE__

var xgds_sample = xgds_sample || {};

$.extend(xgds_sample,{
	initializeSampleEditForm: function(){
		/**
		 * Initialize the sample edit form
		 */
		var _this = this;
		this.updateAdvancedInputFields();
		this.updateNonEditableFields();
		this.toggleAdvancedInput();
		this.setupCollectorInput();
		
		// handler for select box change event.
		$('.sample_info_type').change(function(event){
			$("#id_search_input").val('');
		});
		
		this.getInputFieldsToUpdate();
		// only disable fields if the form save succeeded or it's a new form
		if (fieldsEnabledFlag == 0) {
			this.all_input_fields.prop("disabled", true);
		} else {
			this.onFieldsEnabled();
		}
		
		// handler for 'on enter' event.
		$('.sample_info_type_value').keyup(function(event){
			 if(event.keyCode == 13) {
				 xgds_sample.onEnterLoadSampleInfo(event);
			 }
		});
		
		if (sampleJson) {  // if we get to edit page from sampleview, pull up the info
			// label number and name should be hidden within the form
			this.updateLabelName(hiddenLabel, hiddenName);
			this.postDataLoad(sampleJson);
		}
		
		this.postInit();
	},
	
	postInit: function() {
		
	},
	
	onFieldsEnabled: function() {
		
	},
	
	getFormFieldID: function(jsonKey) {  
		/**
		 * Construct field id from the json key from server
		 */
		return "id_" + jsonKey;
	},
	
	setDomElement: function(id_str, content) {
		var elem = $('#' + id_str);
		if (elem.is("select")) {
			var option_str = '#' + id_str + ' option:first';
			if (content) {
				option_str = '#' + id_str + ' option:contains("' + content + '")';
			} 
			$(option_str).prop('selected', true);
		} else {
			elem.val(content);
		}
	},
 	
	getSampleInfo: function() {
		/**
		 * Fetch the sample info from the server given its label number or name.
		 */
		var url = getSampleInfoUrl;
		var postData = {};
		postData[$("#search_input_type").val()] = $("#id_search_input").val();
		
		var _this = this;
		$.ajax({
			url: url,
			type: "POST",
			data: postData, // serializes the form's elements.
			success: function(data)
			{
				// enable fields
		    	_this.all_input_fields.prop("disabled", false);
		    	
				// clear the error message
				xgds_sample.clearMessages();
				
				// clear all input fields
				_this.all_input_fields.val('');
				
				// insert data sent from the server.
				var json_dict = data[0];
				_this.updateLabelName(json_dict.label_number, json_dict.name);
				_this.updateSampleType(json_dict.sample_type_name);
				var field_elem = undefined;
				for (var key in json_dict) {
					var field_id = _this.getFormFieldID(key);
					var field_elem = $('#' + field_id);
					var field_val = json_dict[key];
					if(field_elem.length != 0) {  // id exists on page.
						_this.setDomElement(field_id, field_val);
					}
				}
				// map and notes
				showOnMap(data);
				_this.updateNotes(json_dict);
				_this.postDataLoad(json_dict);
			},
			error: function(request, status, error) {
				xgds_sample.setMessage(request.responseJSON.message);
			}
		});
	},
	
	updateSampleType: function(name){
		$("#id_sample_type option:contains('" + name + "')").attr('selected','selected');
	},
	
	postDataLoad: function(data){
	},
	
	updateNotes: function(data){
		//TODO if collection_time is null or changes must update
		var container = $('#notes_content');
		xgds_notes.setupNotesUI(container);
		xgds_notes.initializeNotesReference(container, data.app_label, data.model_type, data.pk, data.collection_time, data.collection_timezone);
		xgds_notes.getNotesForObject(data.app_label, data.model_type, data.pk, 'notes_content', container.find('table.notes_list'));
	},
	
	updateLabelName: function(labelNum, sampleName) {
		// copy over the fields into hidden
		$("#id_hidden_name").val(sampleName);
		$("#id_hidden_labelNum").val(labelNum);
		$("#label_number_title").html("<strong> Label number: " + labelNum  + "</strong>");
    	if (_.isNull(sampleName) || sampleName == "") {
			$("#sample_name_title").html("<strong> Name: (Autofills on save) </strong>");
		} else {
			$("#sample_name_title").html("<strong>Name: " + sampleName  + "</strong>");
		}
	},
	
	clearMessages: function() {
		$('.messages').html('<br/>');
		$("#error-message").html('');
	},
	
	setMessage: function(message){
		$("#error-message").html(message);
	},

	onEnterLoadSampleInfo: function(event) {
		/**
		 * On sample name or label number enter,
		 * enable the fields
		 * load sample data (ajax)
		 * (optional) copy over the label number or sample name field into form's hidden fields 
		 */
		// on label number field enter, get the sample info
    	this.clearMessages();
	    	
    	//if it's a name, make sure it passes sanity checks
    	var searchType = $("#search_input_type").val();
    	var searchInput = $("#id_search_input").val();
		var numchars = searchInput.length;
		if (numchars == 0) {
			xgds_sample.setMessage("Cannot search on nothing.");
			return;
		}
    	if (searchType == "sampleName") {
    		if ($.isNumeric(searchInput)) {
    			xgds_sample.setMessage("Sample name cannot be a number.");
    			return;
    		}
    	} else if (! $.isNumeric(searchInput)) {
			xgds_sample.setMessage("Label number must be a number.");
			return;
		}
    	
    	// ajax to get sample info for given label insert into the form.
    	this.getSampleInfo();
	},
	
	setupCollectorInput: function() {
		/**
		 * Autocomplete 'collector' field.
		 */
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
		$('#id_collector_name').typeahead({
			hint: true,
			highlight: true,
			minLength: 1
		},
		{
			name: 'collector_name',
			source: substringMatcher(collectors)
		});
	},
	
	nonEditableFields: ['#id_search_input','#load', '#search_input_type'],
	
	updateNonEditableFields: function() {
		
	},
	
	getInputFieldsToUpdate: function() {
		/**
		 * Get only the input fields inside the form. 
		 */
		this.all_input_fields = $(":input[id^=id_]");
		
		for (var i=0; i<this.nonEditableFields.length; i++){
			this.all_input_fields = this.all_input_fields.not($(this.nonEditableFields[i]));
		}
	},
	
	advancedInputFields: ['#id_lat',
	                      '#id_lon',
	                      '#id_altitude'
	                      ],
	
	updateAdvancedInputFields: function() {
		
	},
	
	toggleAdvancedInput: function() {
		/**
		 * Show or hide the 'out of sim' fields.
		 */
		$.each(this.advancedInputFields, function(index, field){
			$(field).parent().parent().toggle();
		});
		if ($('#id_lat').is(":visible")) {
			$('#toggleInputFields').html('Hide Position');
		} else {
			$('#toggleInputFields').html('Show Position');
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

		$('#id_collector_name').typeahead({
			hint: true,
			highlight: true,
			minLength: 1
		},
		{
			name: 'collector_name',
			source: substringMatcher(collectors)
		});
	}

});
