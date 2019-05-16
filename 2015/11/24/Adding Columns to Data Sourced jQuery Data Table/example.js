$(document).ready(function() {
	var myData = [
		{"name" : "Allen", "dob" : "January 28", "hometown" : "Seattle"},
		{"name" : "Brittany", "dob" : "September 18", "hometown" : "Cleveland"},
		{"name" : "Cedric", "dob" : "December 23", "hometown" : "Boston"},
		{"name" : "Daliah", "dob" : "March 11", "hometown" : "Los Angeles"},
		{"name" : "Ernesto", "dob" : "May 8", "hometown" : "Austin"}
	];

	$("#myTable").DataTable({
		"data" : myData,
		"columns" : [
		{"render" : function() { return '<input type="checkbox">'; }},
		{"data" : "name"},
		{"data" : "dob"},
		{"data" : "hometown"}
		]
	});
});