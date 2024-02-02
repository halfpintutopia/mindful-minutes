(function () {
	let timeElements;
	
	const scheduleEvent = (e) => {
		console.log(e.currentTarget.querySelector('span').innerText);
	};
	
	const initHtmlElements = () => {
		timeElements = document.querySelectorAll('.schedule__timeline li');
	};
	
	const initEvents = () => {
		timeElements.forEach(el => {
			el.addEventListener('click', scheduleEvent);
		});
	};
	
	const init = () => {
		initHtmlElements();
		initEvents();
	};
	
	init();
})();
