$(document).ready(function() {
/*
$(".announce").click(function(){ // Click to only happen on announce links
     $("#cafeId").val($(this).data('id'));
     $('#createFormId').modal('show');
   });*/

	$(".photo").on('click', function() {
		var url = $(this).attr('src');
		$("#modal-image").attr('src', url);
		$("#myModal").modal("show");
	});

});