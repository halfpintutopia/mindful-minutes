const infiniteScrollers = document.querySelectorAll('.infinite-scroller');

if (!window.matchMedia("(prefers-reduced-motion: reduce)").matches) {
    addAnimation();
}

function addAnimation() {
    infiniteScrollers.forEach(function animateScroller(scroller) {
        scroller.setAttribute('data-animated', "true");

        const scrollerInner = scroller.querySelector('.infinite-scroller__inner');

        const scrollerContent = Array.from(scrollerInner.children);

        // Alternatively could you the spread operator e.g. [...scrollerInner.children] as concise and idiomatic but less explicit
        scrollerContent.forEach(function duplicateScrollerItems(item) {
            const duplicatedItem = item.cloneNode(true);
            duplicatedItem.setAttribute('aria-hidden', 'true');
            scrollerInner.appendChild(duplicatedItem);
        });
    });
}