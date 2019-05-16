function ajaxExample1()
{
	var formData = {"name" : $("#nameField").val(), "email" : $("#emailField").val()};

	return $.ajax({
		url : '/myUrl',
		data : formData,
		type : 'POST',
		dataType : 'json'
	});
}

function ajaxExample2(formData)
{
	return $.ajax({
		url : '/myUrl',
		data : formData,
		type : 'POST',
		dataType : 'json'
	});
}

function main()
{
	ajaxExample1().done(function() { ... });

	var formData = {"name" : $("#nameField").val(), "email" : $("#emailField").val()};
	ajaxExample2(formData).done(function() { ... });
}