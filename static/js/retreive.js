
$(document).on('click', '.tabs > li > a', function(e) {
	var $parent = $(this).parent();
	if ($parent.is('.selected')) {
		e.preventDefault();
		// mobile support

		$(this).closest('ul').addClass('active');
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




$('#save_files').click(function()
{
	let final_data = {}
	let image_elements = document.getElementById("image1pic");
	let image_urls = []
	image_urls.push(image_elements.src)

	final_data['images'] = image_urls
	// console.log(image_urls);
	let video_elements = document.getElementById("vid1");
	let video_urls = []

	video_urls.push(video_elements.src)

	final_data['videos'] = video_urls

	let docs_elements = document.getElementById("doc1");
	let docs_urls = []
	docs_urls.push(docs_elements.src)
	final_data['docs'] = docs_urls


	//store ppt links
	let ppt_element = document.getElementById("ppts");
	let ppt_urls = [ppt_element.src];
	console.log(ppt_urls);
	final_data['presentation'] = ppt_urls;
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
	}) .fail(function() {
		alert( "error" );
	})

});


//replace the conatiner element
function replace_urls(element, url){
	element.src = url;
}

//clear the container element
// function clear_element(element){
//
// }
//rebuild containers or replace by clearing the current container
$(document).ready(function(){

	data = JSON.parse(data);
	console.log(data['images'])
	let image_element = document.getElementsByClassName('images');
	replace_urls(image_element, data['images']);
	let video_element = document.getElementById('vid1');
	replace_urls(image_element, data['videos']);
	let docs_element = document.getElementById('doc1');
	replace_urls(docs_element, data['documents']);
	document.getElementById('ppts').src = data['presentation'];
	// replace_urls(ppt_element, data['presentation']);


	// $(".videos").attr("src", data['videos']);
	$(".images").attr("src", data['images']);
	// $(".documents").attr("src", data['documents']);
	// $("#ppts").attr("src", data['presetation']);
});



