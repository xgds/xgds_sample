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

$('#item_labels_table').hide();

$('#show_labels').on('click', function(event) {
	event.preventDefault();
	$('#item_labels_table').toggle();
	if ($('#labels_table').is(":visible")) {
		$('#labels_table').dataTable().resize(); // to resize headers
		$('#show_labels').html("Hide existing labels");
	} else {
		$('#show_labels').html("Show existing labels");
	}
});

// download labels file if available.
if (labelsPdfUrl != "") { 
	$('#download_file').on('click', function(event){
		window.open(labelsPdfUrl,'_blank');
	});
	$('#download_file').click(); // click event is necessary to avoid being blocked by a pop up blocker.
	labelsPdfUrl = "";
}


//$('#print_labels_btn').on('click', function(event) {
//	// validate the form fields (must be integer)
//	var url = printLabelsUrl; // the script where you handle the form input.
//	var postData = $('#print_labels_form').serialize();
//	$.ajax({
//		url: url,
//		type: 'POST',
//		data: postData, // serializes the form's elements.
//		success: function(data)
//		{
//			var labelsDataTable = $('#labels_table').dataTable();
//			var newLabelsArray = [];
//			$(data['newLabels']).each(function() {
//				newLabelsArray.push(JSON.parse(this));
//			});
//			if (newLabelsArray[0] != null) {
//				labelsDataTable.fnAddData(newLabelsArray);
//			} 			    
//			setSaveStatusMessage($('#labels_messages'), data['status'], data['message']);
//		},
//		error: function(request, status, error) {
//			console.log('error ', error);
//		    setSaveStatusMessage($('#labels_messages'), status, error);
//		}
//	});
//	return false; 
//});