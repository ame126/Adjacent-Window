
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

$('#save_files').click(function()
{
	let final_data = {}
	let image_elements = document.getElementsByClassName("images");
	let image_urls = []
	for (let i=0; i < image_elements.length; i++){
		image_urls.push(image_elements[i].src)
	}
	final_data['images'] = image_urls
	// console.log(image_urls);
	let video_elements = document.getElementsByClassName("videos");
	let video_urls = []
	for (let i=0; i < video_elements.length; i++){
		video_urls.push(video_elements[i].src)
	}
	final_data['videos'] = video_urls

	let docs_elements = document.getElementsByClassName("docs");
	let docs_urls = []
	for (let i=0; i < docs_elements.length; i++){
		docs_urls.push(docs_elements[i].src)
	}
	final_data['docs'] = docs_urls


//	store the list input data

	$.ajax({
		type: "POST",
		url: '/save_files',
		data: JSON.stringify(final_data),
		contentType: 'application/json',
		cache: false,
		processData: false
	}).done(function(response){
		console.log(response);

		;
	}) .fail(function() {
		alert( "error" );
	})


});


