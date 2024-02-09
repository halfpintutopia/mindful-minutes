const primaryNavList = document.querySelector('.primary-navigation');
const navToggleButton = document.querySelector('.nav-toggle');

navToggleButton.addEventListener('click', function temp() {
	const visibility = primaryNavList.getAttribute('data-visible');
	if (visibility === 'false') {
		primaryNavList.setAttribute('data-visible', 'true');
		navToggleButton.setAttribute('aria-expanded', 'true');
	} else {
		primaryNavList.setAttribute('data-visible', 'false');
		navToggleButton.setAttribute('aria-expanded', 'false');
	}
});
