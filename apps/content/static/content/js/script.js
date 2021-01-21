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

	$(".reveal-answer").click(function (e) {
		e.preventDefault();

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

	function saveAnswers() {
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

		let userAnswers = {};
		for (i = 0; i < answers.length; i++) {
			questionNum = $(".card")[i].id.split("_")[1];
			answer = answers[i][0] ? answers[i][0] : null;
			userAnswers[questionNum] = answer;
		}

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
				// console.log(data);
			},
		});
	}

	function getPreviousUserAnswers() {
		request = $.ajax({
			url: "/cloud-practitioner-quiz/user-answers/",
			type: "GET",
			headers: {
				"Content-type": "application/json",
				"X-CSRFToken": csrftoken,
			},
			success: function (data) {
				const userAnswers = data;

				const questions = $(".card");
				for (i = 0; i < questions.length; i++) {
					questionNum = questions[i].id.split("_")[1];
					let userAnswer = userAnswers[questionNum];
					$(questions[i])
						.find(`input[value='${userAnswer}']`)
						.prop("checked", true);
				}
			},
		});
	}

	getPreviousUserAnswers();

	$(".saveAnswers").click(function (e) {
		e.preventDefault();
		saveAnswers();

		var targetUrl =
			$(location).attr("href").split("?")[0] + $(this).attr("href");

		setTimeout(function () {
			window.location.href = targetUrl;
		}, 500);
	});

	$("#submitBtn").click(function (e) {
		e.preventDefault();
		saveAnswers();

		setTimeout(function () {
			window.location.href =
				window.location.origin + "/multiple-choice-quiz-results/";
		}, 500);
	});
});
