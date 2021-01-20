$(document).ready(function () {
	function getCookie(name) {
		let cookieValue = null;
		if (document.cookie && document.cookie !== "") {
			const cookies = document.cookie.split(";");
			for (let i = 0; i < cookies.length; i++) {
				const cookie = cookies[i].trim();
				if (cookie.substring(0, name.length + 1) === name + "=") {
					cookieValue = decodeURIComponent(
						cookie.substring(name.length + 1)
					);
					break;
				}
			}
		}
		return cookieValue;
	}
	const csrftoken = getCookie("csrftoken");

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

	$("#btnStart").click(function () {
		$("#overlay").css("display", "none");
		$(".flip-card-inner").css("display", "block");
		$("#btnStart").css("display", "none");
		$(".pagination").css("display", "block");
	});

	$("#submitBtn").click(function (e) {
		e.preventDefault();
		let data = $.map($("input:radio"), function (elem) {
			return $(elem)[0].checked == true ? $(elem).val() : "";
		});

		const choicesPerQuestion = 4;

		let questions = data.reduce((resultArray, item, index) => {
			const chunkIndex = Math.floor(index / choicesPerQuestion);

			if (!resultArray[chunkIndex]) {
				resultArray[chunkIndex] = []; // start a new chunk
			}

			resultArray[chunkIndex].push(item);

			return resultArray;
		}, []);

		let answers = questions.map(function (question) {
			return question.filter((answer) => answer != "");
		});

		var userAnswers = [];
		for (i = 0; i < answers.length; i++) {
			userAnswers.push(answers[i][0]);
		}
		console.log(userAnswers);
		request = $.ajax({
			url: "/cloud-practitioner-quiz/answers/",
			type: "POST",
			headers: {
				"Content-type": "application/json",
				"X-CSRFToken": csrftoken,
			},
			data: JSON.stringify({
				answers: userAnswers,
			}),
			success: function (data) {
				console.log(data);
			},
		});
	});
});
