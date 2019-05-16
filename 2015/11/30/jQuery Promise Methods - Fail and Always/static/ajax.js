$(document).ready(function() {
	$("#myButton").on('click', function() {
		var promised = promiseTest();
		promised.fail(function(data) {
			console.log('promise test');
			alert("FINISHED!");
		});
	});
});


function promiseTest()
{
	return $.ajax({
		url : '/doesnotexist',
		dataType : 'json',
		type : 'POST'
	});
}