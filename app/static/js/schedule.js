const lineHeight = 1;
const start = 0;
const hour = 50;
const week = [
	'Sunday',
	'Monday',
	'Tuesday',
	'Wednesday',
	'Thursday',
	'Friday',
	'Saturday'
];

const suffix = {
	one: 'st',
	two: 'nd',
	few: 'rd',
	other: 'th',
};

let scheduleElement,
	closeBtnElement,
	modalElement,
	dateElement,
	currentDate;

const initDialog = () => {
	modalElement.showModal();
};

const closeDialog = (e) => {
	e.preventDefault();
	modalElement.close();
};

// https://stackoverflow.com/a/69687500/8614652
const initDate = () => {
	const date = new Date();
	const month = new Intl.DateTimeFormat('en-GB', {month: 'long'});
	const day = new Intl.DateTimeFormat('en-GB', {day: 'numeric'});
	const ordinal = new Intl.PluralRules('en-GB', {type: 'ordinal'});
	
	dateElement.innerHTML = `${week[date.getDay()]}, ${day.format(Date.now())}${suffix[ordinal.select(new Date(Date.now()).getDate())]} <span class="uppercase">${month.format(new Date(Date.now()))} ${date.getFullYear()}</span>`;
};

const initHtmlElements = () => {
	scheduleElement = document.querySelectorAll('.schedule__timeline li');
	closeBtnElement = document.querySelector('[data-close-modal]');
	modalElement = document.querySelector('[data-modal]');
	dateElement = document.querySelector('.current-date');
};

const initEvents = () => {
	scheduleElement.forEach(el => {
		el.addEventListener('click', initDialog);
	});
	
	closeBtnElement.addEventListener('click', closeDialog);
	
	
};

const init = () => {
	initHtmlElements();
	initEvents();
	initDate();
};

init();
