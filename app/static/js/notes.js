import { compareOrder, getCurrentDate, removeAllInnerElements } from "./helpers/helpers.js";
import { fetchData, postData } from "./helpers/fetchApi.js";

const server = 'http://localhost:8008';

let editButtonElement,
	doneButtonElement,
	refreshButtonElement,
	addButtonElement,
	modalElement,
	modalCloseButton,
	targetsForm,
	errorMsgElement,
	targetList;

const retrieveTargets = async () => {
	const formData = new FormData(targetsForm);
	const currentDate = getCurrentDate();
	
	const api = `${ server }/api/users/${ formData.get('user') }/target/${ currentDate }/`;
	return await fetchData(api);
};

const createTarget = async (data) => {
	const currentDate = getCurrentDate();
	let dataObj = {};
	
	for (let [ key, value ] of data.entries()) {
		if (key !== 'csrfmiddlewaretoken' && key !== 'user') {
			dataObj[key] = value;
		}
	}
	
	const api = `${ server }/api/users/${ data.get('user') }/target/${ currentDate }/`;
	await postData(api, dataObj, data.get('csrfmiddlewaretoken'));
};

const showDialog = () => {
	modalElement.showModal();
};

const closeDialog = () => {
	modalElement.close();
};

const validateForm = (data) => {
	let valid = true;
	for (let value of data.values()) {
		if (value.trim() === '') {
			valid = false;
		}
	}
	
	return valid;
};

const createTargetEntry = (entry) => {
	const target = `
	        <li class="accordion-list__item">
	            <button data-btn="edit">
	                <i class="fa-regular fa-pen-to-square"></i>
	            </button>
	            <button data-btn="done">
	                <span></span>
	            </button>
	            <p class="handwritten">${ entry.title }</p>
	        </li>
	    `;
	
	targetList.insertAdjacentHTML("beforeend", target);
};




const showTargets = () => {
	retrieveTargets()
		.then(res => {
			res.sort(compareOrder);
			removeAllInnerElements(targetList);
			res.forEach(target => {
				createTargetEntry(target);
			});
		});
};

// TODO change to appropriate name after refactoring
const temp = () => {
	
	
	// on delete, send delete request to api
};

const showForm = () => {
	showDialog();
};

const sendForm = (e) => {
	e.preventDefault();
	// on save, collect form data
	const formData = new FormData(targetsForm);
	if (validateForm(formData)) {
		createTarget(formData)
			.then(r => {
				showTargets();
				closeDialog();
			});
	} else {
		errorMsgElement.innerText = `You haven't provided enough information, please fill in the form`;
	}
	// send to api to create
	// clear form
	// close the modal
	// add target to list on day targets
	// add the edit button
	// add the done / refresh button
};

const initHtmlElements = () => {
	editButtonElement = document.querySelectorAll('[data-btn="target-edit"]');
	doneButtonElement = document.querySelectorAll('[data-btn="target-done"]');
	addButtonElement = document.querySelector('[data-btn="target-add"]');
	modalElement = document.querySelector('[data-modal="targets"]');
	modalCloseButton = document.querySelector('form#targets [data-btn="close"]');
	targetsForm = document.querySelector('form#targets');
	errorMsgElement = document.querySelector('form#targets .error-msg');
	targetList = document.querySelector('[data-accordion-list="targets"]');
};

const initEvents = () => {
	addButtonElement.addEventListener('click', showForm);
	modalCloseButton.addEventListener('click', closeDialog);
	targetsForm.addEventListener('submit', sendForm);
};

const init = () => {
	initHtmlElements();
	initEvents();
	showTargets();
};

init();