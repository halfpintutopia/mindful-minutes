import {getCurrentDate} from "./helpers/helpers.js";
import {fetchData, postData} from "./helpers/fetchApi.js";

const lineHeight = 1;
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
	scheduleEventListItemsElement,
	closeBtnElement,
	modalElement,
	dateElement,
	scheduleForm,
	errorMsgElement,
	submitBtnElement;

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
		console.log(entry);
		const timeFromArray = entry.time_from.split(':');
		const timeUntilArray = entry.time_until.split(':');
		const duration = timeUntilArray[0] - timeFromArray[0];
		const item = document.createElement('li');
		
		item.innerText = entry.title;
		item.setAttribute('data-time-from', entry.time_from);
		item.setAttribute('data-time-until', entry.time_until);
		item.setAttribute('data-title', entry.title);
		item.setAttribute('data-entry-id', entry.id);
		item.style.top = `${timeFromArray[0] * hour - lineHeight}px`;
		item.style.height = `${duration * hour + lineHeight}px`;
		item.addEventListener('click', initDialog);
		scheduleEventListElement.append(item);
	});
};

const initSchedule = async () => {
	let child = scheduleEventListElement.lastElementChild;
	while (child) {
		scheduleEventListElement.removeChild(child);
		child = scheduleEventListElement.lastElementChild;
	}
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

const initDialog = (e) => {
	modalElement.showModal();
	if (e.currentTarget.dataset.title) {
		const timeFromArray = e.currentTarget.dataset.timeFrom.split(':');
		const timeUntilArray = e.currentTarget.dataset.timeUntil.split(':');
		document.querySelector('input#title').value = e.currentTarget.dataset.title;
		document.querySelector('select#time-from').selectedIndex = timeFromArray[0];
		document.querySelector('select#time-until').selectedIndex = timeUntilArray[0] - 1;
		
		scheduleForm.setAttribute('data-entry-id', e.currentTarget.dataset.entryId);
		// document.querySelector('input#tile').value = e.currentTarget.dataset.title;
	}
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
	const currentDate = getCurrentDate();
	const dataObj = {
		'date': currentDate,
		'title': formData.get('title'),
		'time_from': formData.get('timeFrom'),
		'time_until': formData.get('timeUntil'),
	};
	
	if (checkTimes(formData)) {
		let api;
		if (e.currentTarget.dataset.entryId) {
			api = `${server}/api/users/${formData.get('user')}/appointments/${currentDate}/${e.currentTarget.dataset.entryId}/`;
			await postData(api, dataObj, formData.get('csrfmiddlewaretoken'), 'PUT');
			initSchedule();
		} else {
			api = `${server}/api/users/${formData.get('user')}/appointments/${currentDate}/`;
			await postData(api, dataObj, formData.get('csrfmiddlewaretoken'));
		}
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
	// submitBtnElement = document.querySelector('button[type="submit"]');
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
