(function () {
	const primaryNavList = document.querySelector('.primary-navigation');
	const navToggleButton = document.querySelector('.nav-toggle');
	
	const header = document.querySelector('.primary-header');
	const headerHeight = header.offsetHeight;
	console.log('heights', header.offsetHeight, header.clientHeight);
	
	document.documentElement.style.setProperty('--header-height', `${headerHeight}px`);
	
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
})();