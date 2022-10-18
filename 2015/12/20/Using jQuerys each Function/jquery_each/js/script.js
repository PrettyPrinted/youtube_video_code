$(document).ready(function() {

	$("#randomize").on('click', function() {



		$(".progress-bar").each(function() {
			
			var randomPct = Math.round(Math.random() * 100);

			$(this).attr("aria-valuenow", randomPct);
			$(this).css("width", randomPct + "%");
			$(this).text(randomPct + "%");
			
		});


	});

});