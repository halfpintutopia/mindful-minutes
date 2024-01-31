// https://codepen.io/monbrielle/pen/dyYRgPm
// https://www.youtube.com/watch?v=VdqtdKXxKhM&list=PLjY7XQnia3s5x9VepvUha4v4T0wELnFmR&index=4&t=2064s
(function () {
	
	const pages = document.querySelectorAll('.form-page');
	const pageList = Array.from(pages);
	const formNavButtons = document.querySelector('.btn-form-direction-wrapper');
	const previousBtn = formNavButtons.querySelector('[data-form-direction="up"]');
	const nextBtn = formNavButtons.querySelector('[data-form-direction="down"]');
	const continueButtons = document.querySelectorAll('.btn-continue');
	
	let currentPage, incrementor, warningMsg;
	
	function showCurrentPage() {
		pages.forEach(function toggleActivePage(page, index) {
			page.toggleAttribute('data-form-page-active', index === currentPage);
		});
	}
	
	function checkInputs() {
		const inputs = pages[currentPage].querySelectorAll("input");
		const inputList = Array.from(inputs);
		
		// or use the arrow function with an implicit return behaviour
		return inputList.every(function checkInputIsValid(input) {
			if (!input.checkValidity()) {
				warningMsg = `Don't forget to add your ${input.getAttribute("name").replace("_", " ")}`;
				input.nextElementSibling.innerText = warningMsg;
			}
			return input.checkValidity();
		});
	}
	
	function showHideFormNavButton() {
		nextBtn.toggleAttribute('disabled', currentPage === pages.length - 1);
		previousBtn.toggleAttribute('disabled', currentPage === 0);
	}
	
	currentPage = pageList.findIndex(function getActivePage(page) {
		return page.getAttribute('data-form-page-active');
	});
	
	if (currentPage < 0) {
		currentPage = 0;
		showCurrentPage();
		showHideFormNavButton();
	}
	
	function changeCurrentPage(event) {
		event.preventDefault();
		if (event.currentTarget.matches('[data-form-direction="down"]')) {
			incrementor = 1;
			if (checkInputs()) {
				currentPage += incrementor;
				showCurrentPage();
				showHideFormNavButton();
			}
		} else if (event.currentTarget.matches('[data-form-direction="up"]')) {
			incrementor = -1;
			currentPage += incrementor;
			showCurrentPage();
			showHideFormNavButton();
		}
	}
	
	continueButtons.forEach((button, index) => {
		button.addEventListener('click', changeCurrentPage);
	});
	
	nextBtn.addEventListener('click', changeCurrentPage);
	previousBtn.addEventListener('click', changeCurrentPage);
})();