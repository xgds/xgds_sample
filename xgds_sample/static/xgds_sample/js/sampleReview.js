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

function setChangedPosition(value, container) {
	$(container).find('#id_changed_position').attr('value', value);
}


/**
 * Set the changed_position to true if the user edits any of the position fields.
 * @param container
 */
function hookEditingPosition(container) {
	$(container).find("#id_latitude").change(function() {setChangedPosition(1, container)});
	$(container).find("#id_longitude").change(function() {setChangedPosition(1, container)});
	$(container).find("#id_altitude").change(function() {setChangedPosition(1, container)});
}


function showOnMap(data){
	app.vent.trigger("mapSearch:found", data);
	app.vent.trigger('mapSearch:fit');
}