$(document).on('click', '.tabs > li > a', function(e) {
	var $parent = $(this).parent();
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