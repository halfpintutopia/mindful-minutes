import {getCurrentDate} from "./helpers/helpers.js";
import {fetchData, postData} from "./helpers/fetchApi.js";

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

const server = 'http://localhost:8008';

let scheduleElement,
	scheduleEventListElement,
	closeBtnElement,
	modalElement,
	dateElement,
	scheduleForm,
	errorMsgElement;

const createTimeOptions = (start, end, el) => {
	let option;
	
	while (start < end) {
		if (start < 10) {
			option = new Option(`0${start}:00`, `0${start}:00`);
		} else {
			option = new Option(`${start}:00`, `${start}:00`);
		}
		el.add(option, undefined);
		
		start++;
	}
};

const createEntries = (entries) => {
	entries.map(entry => {
		// Convert the time to placement in increments of 50px per hour down
		const timeFromArray = entry.time_from.split(':');
		// console.log(`top: ${top - lineHeight}px`);
		// Convert length of time time-until delete time-from and covert to height of div 50px per hour
		const timeUntilArray = entry.time_until.split(':');
		
		const duration = timeUntilArray[0] - timeFromArray[0];
		
		const item = document.createElement('li');
		item.innerText = entry.title;
		item.style.top = `${timeFromArray[0] * hour - lineHeight}px`;
		item.style.height = `${duration * hour + lineHeight}px`;
		
		scheduleEventListElement.append(item);
	});
};

const initSchedule = async () => {
	const formData = new FormData(scheduleForm);
	const currentDate = getCurrentDate();
	
	const api = `${server}/api/users/${formData.get('user')}/appointments/${currentDate}/`;
	const data = await fetchData(api);
	createEntries(data);
};

const initTimeSelectElement = () => {
	const timeFromInput = document.querySelector('select#time-from');
	const timeUntilInput = document.querySelector('select#time-until');
	createTimeOptions(0, 24, timeFromInput);
	createTimeOptions(1, 25, timeUntilInput);
};

const initDialog = () => {
	modalElement.showModal();
};

const closeDialog = (e) => {
	e.preventDefault();
	modalElement.close();
};

const checkTimes = (data) => {
	return data.get('timeFrom') < data.get('timeUntil');
};

const sendData = async (e) => {
	e.preventDefault();
	
	const formData = new FormData(scheduleForm);
	if (checkTimes(formData)) {
		const currentDate = getCurrentDate();
		
		const dataObj = {
			'date': currentDate,
			'title': formData.get('title'),
			'time_from': formData.get('timeFrom'),
			'time_until': formData.get('timeUntil'),
		};
		
		const api = `${server}/api/users/${formData.get('user')}/appointments/${currentDate}/`;
		await postData(api, dataObj, formData.get('csrfmiddlewaretoken'));
		closeDialog(e);
	} else {
		errorMsgElement.innerText = "A task or appointment can't finish before it starts, unless you're the Flash?";
	}
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
	scheduleEventListElement = document.querySelector('.event-list');
	closeBtnElement = document.querySelector('[data-close-modal]');
	modalElement = document.querySelector('[data-modal]');
	dateElement = document.querySelector('.current-date');
	scheduleForm = document.querySelector('form#schedule');
	errorMsgElement = document.querySelector('form .error-msg');
};

const initEvents = () => {
	scheduleElement.forEach(el => {
		el.addEventListener('click', initDialog);
	});
	
	closeBtnElement.addEventListener('click', closeDialog);
	
	scheduleForm.addEventListener('submit', sendData);
};

const init = () => {
	initHtmlElements();
	initEvents();
	initDate();
	initTimeSelectElement();
	initSchedule();
};

init();
