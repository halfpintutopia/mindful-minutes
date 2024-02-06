(function () {
	const lineHeight = 1;
	
	
	let timeElements,
		closeBtn,
		modal;
	
	const initDialog = () => {
		modal.showModal();
	};
	
	const closeDialog = () => {
		modal.close();
	};
	
	const initHtmlElements = () => {
		timeElements = document.querySelectorAll('.schedule__timeline li');
		closeBtn = document.querySelector('[data-close-modal]');
		modal = document.querySelector('[data-modal]');
	};
	
	const initEvents = () => {
		timeElements.forEach(el => {
			el.addEventListener('click', initDialog);
		});
		
		closeBtn.addEventListener('click', closeDialog);
	};
	
	const init = () => {
		initHtmlElements();
		initEvents();
	};
	
	init();
})();
