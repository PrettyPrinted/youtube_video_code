$(document).ready(function() {
	$("#myButton").on('click', function() {
		var promised = promiseTest();
		promised.done(function(data) {
			console.log('promise test');
			alert(data.result);
		});
	});
});

function successTest()
{
	$.ajax({
		url : '/ajaxtest',
		dataType : 'json',
		type : 'POST',
		success : function(data) {
			console.log("successTest");
			alert(data.result);
		}
	});
}

function promiseTest()
{
	return $.ajax({
		url : '/ajaxtest',
		dataType : 'json',
		type : 'POST'
	});
}