$(document).ready(function(){
	$(function() {
		console.log("inside");
		$('#searchsubmit').click(function(){
			q = $('#search').val();
			console.log("calling function")
			getIc50(q);
	});
});
})