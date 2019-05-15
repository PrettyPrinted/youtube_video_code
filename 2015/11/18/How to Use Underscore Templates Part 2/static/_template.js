$(document).ready(function() {

  var myTemplate = _.template($("#template").html());

  $("#clickMe").click(function() {
  	 var userValues = {
  	 	make : $("#make").val(),
  	 	model : $("#model").val(),
  	 	trim : $("#trim").val()
  	 }

  	 $("#appendHere").append(myTemplate(userValues));

  	 $("#make").val("");
  	 $("#model").val("");
  	 $("#trim").val("");
  });

});
