(function () {
	// function calculateHeaderHeight() {
	const header = document.querySelector('.header-wrapper');
	const rect = header.getBoundingClientRect();
	
	const headerHeight = header.offsetHeight;
	
	document.documentElement.style.setProperty('--header-height', `${headerHeight}px`);
	
	// }
	//
	// addEventListener('resize', () => {
	// });
})();
