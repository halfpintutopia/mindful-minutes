(function () {
	const calculateHeaderHeight = () => {
		const header = document.querySelector('.header-base');
		const rect = header.getBoundingClientRect();
		
		const headerHeight = header.offsetHeight;
		console.log('heights', header.offsetHeight, header.clientHeight, rect.height);
		
		document.documentElement.style.setProperty('--header-height', `${headerHeight}px`);
		
	};
	
	window.addEventListener('resize', calculateHeaderHeight);
})();
