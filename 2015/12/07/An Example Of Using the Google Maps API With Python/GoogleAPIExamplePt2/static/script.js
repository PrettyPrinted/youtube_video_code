$(document).ready(function() {

  $("#search").click(function() {
    var searchReq = $.get("/sendRequest/" + $("#query").val());
    searchReq.done(function(data) {
       $("#image").html(data);
    });
  });

});