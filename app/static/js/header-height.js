(function () {
	// function calculateHeaderHeight() {
	console.log('hello');
	const header = document.querySelector('.header-wrapper');
	const rect = header.getBoundingClientRect();
	
	const headerHeight = header.offsetHeight;
	console.log('heights', header.offsetHeight, header.clientHeight, rect.height);
	
	document.documentElement.style.setProperty('--header-height', `${headerHeight}px`);
	
	// }
	//
	// addEventListener('resize', () => {
	// 	console.log("hello");
	// });
})();
