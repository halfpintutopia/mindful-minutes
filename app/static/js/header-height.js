(function () {
	const header = document.querySelector('.header-wrapper');
	
	const headerHeight = header.offsetHeight;
	
	document.documentElement.style.setProperty('--header-height', `${headerHeight}px`);
})();
