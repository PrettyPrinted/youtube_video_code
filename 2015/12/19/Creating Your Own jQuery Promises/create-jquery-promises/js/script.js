$(document).ready(function() {

	var myPromise = createPromise();

	myPromise.done(function() {
		$("#success-alert").show();
	});

	myPromise.fail(function() {
		$("#fail-alert").show();
	});

});

function createPromise() {
	var myDeferred = $.Deferred();

	$('#success').on('click', function() {
		myDeferred.resolve();
	});

	$('#fail').on('click', function() {
		myDeferred.reject();
	});

	return myDeferred.promise();
}