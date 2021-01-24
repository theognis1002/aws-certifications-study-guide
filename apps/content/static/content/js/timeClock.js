$(document).ready(function () {
	function startTimer() {
		var diff, hours, minutes, seconds;
		const endTimeUTC = new Date(
			Date.UTC(
				endTime.getFullYear(),
				endTime.getMonth(),
				endTime.getDate(),
				endTime.getHours(),
				endTime.getMinutes(),
				endTime.getSeconds()
			)
		);

		function timer() {
			const date = new Date();
			const timestampUTC = new Date(
				Date.UTC(
					date.getUTCFullYear(),
					date.getUTCMonth(),
					date.getUTCDate(),
					date.getUTCHours(),
					date.getUTCMinutes(),
					date.getUTCSeconds()
				)
			);

			diff = ((endTimeUTC - timestampUTC) / 1000) | 0;

			hours = (diff / 3600) | 0;
			minutes = ((diff % 3600) / 60) | 0;
			seconds = diff % 60 | 0;

			hours = hours < 10 ? "0" + hours : hours;
			minutes = minutes < 10 ? "0" + minutes : minutes;
			seconds = seconds < 10 ? "0" + seconds : seconds;
			console.log(hours, minutes, seconds);
			$("#timeClock").text(hours + ":" + minutes + ":" + seconds);
		}
		timer();
		setInterval(timer, 1000);
	}

	startTimer();
});
