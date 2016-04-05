function setSaveStatusMessage(handler, status, msg){
	if (status == 'success') {
		handler.attr('class', 'success-message');
	} else {
		handler.attr('class', 'error-message');
	}
	handler.html(msg);
	setTimeout(function() { // messages fades out.
		handler.fadeOut().empty();
	}, 5000);
}

$('#create_labels_btn').on('click', function(event) {
	event.preventDefault(); 	// avoid to execute the actual submit of the form.
	// validate the form fields (must be integer)
	var url = createLabelUrl; // the script where you handle the form input.
	var postData = $('#create_labels_form').serialize();
	$.ajax({
		url: url,
		type: 'POST',
		data: postData, // serializes the form's elements.
		success: function(data)
		{
			var labelsDataTable = $('#labels_table').dataTable();
			var newLabelsArray = [];
			$(data['newLabels']).each(function() {
				newLabelsArray.push(JSON.parse(this));
			});
			if (newLabelsArray[0] != null) {
				labelsDataTable.fnAddData(newLabelsArray);
			} 			    
			setSaveStatusMessage($('#labels_messages'), data['status'], data['message']);
		},
		error: function(request, status, error) {
			console.log('error ', error);
		    setSaveStatusMessage($('#labels_messages'), status, error);
		}
	});
	return false; 
});