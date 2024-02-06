const lineHeight = 1;
const start = 0;
const hour = 50;

let timeElements,
	closeBtn,
	modal;

const initDialog = () => {
	modal.showModal();
};

const closeDialog = (e) => {
	e.preventDefault();
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
