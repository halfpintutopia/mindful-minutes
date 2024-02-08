let editButtonElement,
	doneButtonElement,
	refreshButtonElement,
	addButtonElement,
modal;

// TODO change to appropriate name after refactoring
const temp = () => {
	// Open a new dialog
	modal.showModal();
	// the dialog contains
	//  - a form
	//  - save and delete buttons
};

const initHtmlElements = () => {
	editButtonElement = document.querySelectorAll('[data-btn="note-edit"]');
	doneButtonElement = document.querySelectorAll('[data-btn="note-done"]');
	addButtonElement = document.querySelector('[data-btn="note-add"]');
	modal = document.querySelector('[data-modal="notes"]');
};

const initEvents = () => {
	addButtonElement.addEventListener('click', temp);
};

const init = () => {
	initHtmlElements();
	initEvents();
};

init();