$(document).ready(function () {
	if (firstPage) {
		$("#overlay").css("display", "block");
		$(".flip-card-inner").css("display", "none");
	} else {
		$(".pagination").css("display", "block");
	}
});
