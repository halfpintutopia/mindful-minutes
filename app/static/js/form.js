// https://codepen.io/monbrielle/pen/dyYRgPm
(function () {

    const form = document.querySelector('form');
    const formCloseButton = document.querySelector('.form-header__close');
    const nextButtons = document.querySelectorAll('.next');
    const pages = document.querySelectorAll('.form-page');
    const pageList = Array.from(pages);

    // Get the root element
    const cssRoot = document.querySelector(':root');
    let currentPage, nextPage, previousPage, opacity, current = 1, progress;

    // https://stackdiary.com/tutorials/prevent-form-submission-on-pressing-enter-with-javascript/
    form.addEventListener('keypress', function preventSubmitting(event) {
        if (event.key === 'Enter') {
            event.preventDefault();
        }
    });

    formCloseButton.addEventListener('click', function returnToPreviousPage() {
        history.go(-1);
    });

    nextButtons.forEach(function addClickEvent(btn) {
        btn.addEventListener('click', function addActiveClass() {
            currentPage = this.closest('.form-page[data-form-page-position="active"]');
            nextPage = currentPage.nextElementSibling;

            if (pageList.indexOf(nextPage) < pageList.length) {
                progress = (pageList.indexOf(nextPage) / pages.length) * 100;
                cssRoot.style.setProperty('--progress', `${progress}%`);

                currentPage.dataset.formPagePosition = "above";
                nextPage.dataset.formPagePosition = 'active';
                if (pageList.indexOf(nextPage) === pages.length - 1) {
                    form.dataset.currentPage = 'last';
                } else {
                    form.dataset.currentPage = `${pageList.indexOf(nextPage) + 1}`;
                }
            }
        });
    });

    const formNavigationPreviousBtn = document.querySelector('.btn-previous');
    const formNavigationNextBtn = document.querySelector('.btn-next');

    formNavigationPreviousBtn.addEventListener('click', function navigateUp() {
        currentPage = this.closest('.main-form').querySelector('.form-page[data-form-page-position="active"]');

        if (pageList.indexOf(currentPage) > 0) {
            previousPage = currentPage.previousElementSibling;

            progress = (pageList.indexOf(previousPage) / pages.length) * 100;
            cssRoot.style.setProperty('--progress', `${progress}%`);

            currentPage.dataset.formPagePosition = "below";
            previousPage.dataset.formPagePosition = 'active';

            if (pageList.indexOf(previousPage) === 0) {
                form.dataset.currentPage = '1';
            } else {
                form.dataset.currentPage = `${pageList.indexOf(previousPage) + 1}`;
            }
        }
    });

    formNavigationNextBtn.addEventListener('click', function navigateUp() {
        currentPage = this.closest('.main-form').querySelector('.form-page[data-form-page-position="active"]');

        if (pageList.indexOf(currentPage) > 0) {
            nextPage = currentPage.nextElementSibling;

            progress = (pageList.indexOf(nextPage) / pages.length) * 100;
            cssRoot.style.setProperty('--progress', `${progress}%`);

            currentPage.dataset.formPagePosition = "above";
            nextPage.dataset.formPagePosition = 'active';

            if (pageList.indexOf(nextPage) === pages.length - 1) {
                form.dataset.currentPage = 'last';
            } else {
                form.dataset.currentPage = `${pageList.indexOf(nextPage) + 1}`;
            }
        }
    });

})();