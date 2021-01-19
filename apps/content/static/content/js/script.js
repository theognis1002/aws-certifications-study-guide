$(document).ready(function () {
	$(".reveal-answer").click(function () {
		if ($(this).hasClass("btn-primary")) {
			let answer = $(this).siblings(".answer").val();
			$(this).text(answer);
			$(this).removeClass("btn-primary").addClass("btn-success");
		} else {
			$(this).text("Reveal Answer");
			$(this).removeClass("btn-success").addClass("btn-primary");
		}
	});

	$("#overlay").click(function () {
		$("#overlay").css("display", "none");
		$(".flip-card-inner").css("display", "block");
	});

	if (firstPage) {
		$("#overlay").css("display", "block");
		$(".flip-card-inner").css("display", "none");
	}
});
