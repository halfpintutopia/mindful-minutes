const accordions = document.querySelectorAll('.accordion');

accordions.forEach(accordion => {
	accordion.addEventListener('click', (e) => {
		const activePanel = e.target.closest('.accordion-panel');
		if (!activePanel) return;
		toggleAccordion(activePanel);
	});
	
	function toggleAccordion(panelToActivate) {
		const buttons = panelToActivate.parentElement.querySelectorAll('button');
		const contents = panelToActivate.parentElement.querySelectorAll('.accordion-content');
		
		buttons.forEach(button => {
			button.setAttribute('aria-expanded', "false");
		});
		
		contents.forEach(button => {
			button.setAttribute('aria-hidden', "true");
		});
		
		panelToActivate.querySelector('button').setAttribute('aria-expanded', 'true');
		panelToActivate.querySelector('.accordion-content').setAttribute('aria-content', 'false');
	}
});
