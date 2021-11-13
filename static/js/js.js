
$(document).on('click', '.tabs > li > a', function(e) {
	var $parent = $(this).parent();
	console.log($parent);
	console.log(e)
	if ($parent.is('.selected')) {
		e.preventDefault();
		// mobile support
		$(this).closest('ul').addClass('active');
	} else {
		var target = $(this).attr('href');
		$(target).siblings().removeClass('selected');
		$(target).addClass('selected');

		$parent.siblings().removeClass('selected');
		$parent.addClass('selected');
		// mobile support
		$(this).closest('ul').removeClass('active');
	}
});


$('#upload_form').submit(function(e) {
	e.preventDefault();
	var form_data = new FormData($('#upload_form')[0]);
	$.ajax({
		type: "POST",
		url: '/upload',
		data: form_data,
		contentType: false,
		cache: false,
		processData: false
	}).done(function(response){
			console.log(response);
			message = "File Uploaded Successfully"
			// window.alert("File Uploaded Successfully" );
		})

});


