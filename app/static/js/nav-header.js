if (document.querySelector('.header-wrapper') !== null) {
	const header = document.querySelector('.header-wrapper');
	const scrollWatcher = document.createElement('div');
	const headerHeight = header.offsetHeight;
	
	scrollWatcher.setAttribute('data-scroll-watcher', '');
	header.before(scrollWatcher);
	
	const navObserver = new IntersectionObserver(
		(entries) => {
			header.classList.toggle('sticking', !entries[0].isIntersecting);
		},
		{rootMargin: '50px 0px 0px 0px'}
	);
	
	navObserver.observe(scrollWatcher);
	
	document.documentElement.style.setProperty('--header-height', `${headerHeight}px`);
}
