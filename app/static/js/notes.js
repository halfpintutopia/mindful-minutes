import { compareOrder, getCurrentDate, removeAllInnerElements } from "./helpers/helpers.js";
import { fetchData, postData } from "./helpers/fetchApi.js";

const server = 'http://localhost:8008';

let editButtons,
  doneButtons,
  refreshButtonElement,
  addButtonElement,
  modalElement,
  modalCloseButton,
  targetsForm,
  errorMsgElement,
  targetList;

const retrieveTargets = async () => {
  const formData = new FormData(targetsForm);
  const currentDate = getCurrentDate();
  
  const api = `${ server }/api/users/${ formData.get('user') }/target/${ currentDate }/`;
  return await fetchData(api);
};

const createTarget = async (data) => {
  const currentDate = getCurrentDate();
  const dataObj = createDataObject(data);
  
  const api = `${ server }/api/users/${ data.get('user') }/target/${ currentDate }/`;
  await postData(api, dataObj, data.get('csrfmiddlewaretoken'));
};

const updateTarget = async (data) => {
  const currentDate = getCurrentDate();
  const dataObj = createDataObject(data);
  
  const api = `${ server }/api/users/${ data.get('user') }/target/${ currentDate }/${ targetsForm.dataset.formEntryId }/`;
  await postData(api, dataObj, data.get('csrfmiddlewaretoken'), 'PUT');
};

const createDataObject = (data) => {
  let dataObj = {};
  for (let [ key, value ] of data.entries()) {
    if (key !== 'csrfmiddlewaretoken' && key !== 'user') {
      dataObj[key] = value;
    }
  }
  return dataObj;
};

const showDialog = () => {
  modalElement.showModal();
};

const closeDialog = () => {
  modalElement.close();
};

const addFormId = (id) => {
  targetsForm.dataset.formEntryId = id;
};

const removeFormId = () => {
  targetsForm.dataset.formEntryId = undefined;
};

const validateForm = (data) => {
  let valid = true;
  for (let value of data.values()) {
    if (value.trim() === '') {
      valid = false;
    }
  }
  
  return valid;
};

const createTargetEntry = (entry) => {
  const target = `
    <li class="accordion-list__item" data-entry-id="${ entry.id }" data-entry-order="${ entry.order }" data-entry-title="${ entry.title }">
      <button data-btn="edit">
          <i class="fa-regular fa-pen-to-square"></i>
      </button>
      <button data-btn="done">
          <span></span>
      </button>
      <p class="handwritten">${ entry.title }</p>
    </li>
`;
  
  targetList.insertAdjacentHTML("beforeend", target);
};

const showTargets = () => {
  retrieveTargets()
    .then(res => {
      try {
        res.sort(compareOrder);
        removeAllInnerElements(targetList);
        res.forEach(target => {
          createTargetEntry(target);
        });
      } catch (error) {
        console.error(error);
      }
    })
    .then(() => {
      editButtons = document.querySelectorAll('[data-btn="edit"]');
      editButtons.forEach(btn => {
        btn.addEventListener('click', fillForm);
      });
      
      doneButtons = document.querySelectorAll('[data-btn="done"]');
      doneButtons.forEach(btn => {
        btn.addEventListener('click', markAndUTargetAsDone);
      });
    });
};

const markAndUTargetAsDone = (e) => {
  const target = e.currentTarget;
  if (target.dataset.btn === 'done') {
    target.dataset.btn = 'refresh';
    target.nextElementSibling.classList.add('done');
  } else {
    target.dataset.btn = 'done';
    target.nextElementSibling.classList.remove('done');
  }
};

const fillForm = (e) => {
  const formData = new FormData(targetsForm);
  const item = e.currentTarget.closest('.accordion-list__item');
  
  for (let [ key, value ] of formData.entries()) {
    if (key !== 'csrfmiddlewaretoken' && key !== 'user') {
      const input = targetsForm.querySelector(`[name=${ key }]`);
      const dataValue = item.getAttribute(`data-entry-${ key }`);
      if (input) {
        input.value = dataValue;
      }
    }
  }
  addFormId(item.dataset.entryId);
  showDialog();
};

const showForm = () => {
  showDialog();
};

const sendForm = (e) => {
  e.preventDefault();
  const formData = new FormData(targetsForm);
  if (validateForm(formData)) {
    if (targetsForm.dataset.formEntryId) {
      updateTarget(formData)
        .then(r => {
          showTargets();
          closeDialog();
        });
    } else {
      createTarget(formData)
        .then(r => {
          showTargets();
          closeDialog();
        });
    }
  } else {
    errorMsgElement.innerText = `You haven't provided enough information, please fill in the form`;
  }
};

const initHtmlElements = () => {
  addButtonElement = document.querySelector('[data-btn="target-add"]');
  modalElement = document.querySelector('[data-modal="targets"]');
  modalCloseButton = document.querySelector('form#targets [data-btn="close"]');
  targetsForm = document.querySelector('form#targets');
  errorMsgElement = document.querySelector('form#targets .error-msg');
  targetList = document.querySelector('[data-accordion-list="targets"]');
};

const initEvents = () => {
  addButtonElement.addEventListener('click', showForm);
  modalCloseButton.addEventListener('click', closeDialog);
  targetsForm.addEventListener('submit', sendForm);
};

const init = () => {
  initHtmlElements();
  initEvents();
  showTargets();
};

init();