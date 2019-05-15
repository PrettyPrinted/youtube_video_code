$(document).ready(function() {
  count = 1;
  var myTemplate = _.template("<p><%= c %></p>");

  $("#myButton").click(function() {
      var newElement = myTemplate({ c : count });
      $("#myDiv").append(newElement);
      count++;
  });

});