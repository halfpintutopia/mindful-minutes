import { compareOrder, createUrl, getCurrentDate, removeAllInnerElements } from "./helpers/helpers.js";
import { fetchData, postData } from "./helpers/fetchApi.js";
import { activateLoader, deactivateLoader } from "./helpers/loader.js";

const errorMessage = `You haven't provided enough information, please fill in the form`;

let refreshButtonElement,
  addButtonElement,
  modalElement,
  modalCloseButton,
  targetsForm,
  errorMsgElement,
  targetList,
  deleteBtnElement;

const showDeleteBtn = () => {
  deleteBtnElement.style.visibility = "visible";
};

const hideDeleteBtn = () => {
  deleteBtnElement.style.visibility = "hidden";
};

const retrieveTargets = async () => {
  const formData = new FormData(targetsForm);
  const currentDate = getCurrentDate();
  
  const api = createUrl(`/api/users/${ formData.get('user') }/target/${ currentDate }/`);
  return await fetchData(api);
};

const createTarget = async (data) => {
  activateLoader('create');
  const currentDate = getCurrentDate();
  const dataObj = createDataObject(data);
  
  const api = createUrl(`/api/users/${ data.get('user') }/target/${ currentDate }/`);
  await postData(api, dataObj, data.get('csrfmiddlewaretoken'));
  deactivateLoader('Day target entry', 'create');
};

const updateTarget = async (data) => {
  activateLoader('update');
  const formData = new FormData(targetsForm);
  formData.append("completed", data.dataset.completed === 'true' ? "True" : "False")
  const currentDate = getCurrentDate();
  
  const dataObj = createDataObject(formData);
  
  const api = createUrl(`/api/users/${ formData.get('user') }/target/${ currentDate }/${ data.dataset.id }/`);
  await postData(api, dataObj, formData.get('csrfmiddlewaretoken'), 'PUT');
  deactivateLoader('Day target entry', 'update');
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
  removeErrorMsg();
  modalElement.showModal();
};


const closeDialog = () => {
  modalElement.close();
};

const removeErrorMsg = () => {
  errorMsgElement.innerText = '';
}

const addFormId = (id) => {
  targetsForm.dataset.entryId = id;
};

const removeFormId = () => {
  targetsForm.dataset.formEntryId = undefined;
};

const validateForm = (data) => {
  let valid = true;
  for (let [ key, value ] of data) {
    if (value.trim() === '') {
      valid = false;
    }
  }
  
  return valid;
};

const resetForm = () => {
  targetsForm.reset();
};

const createTargetEntry = (entry) => {
  const target = `
    <li
    class="accordion-list__item"
    data-id="${ entry.id }"
    data-order="${ entry.order }"
    data-title="${ entry.title }"
    data-completed="${ entry.completed }"
    >
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
      const editButtons = document.querySelectorAll('[data-btn="edit"]');
      editButtons.forEach(btn => {
        btn.addEventListener('click', fillForm);
      });
      
      const doneButtons = document.querySelectorAll('[data-btn="done"]');
      doneButtons.forEach(btn => {
        btn.addEventListener('click', toggleTargetCompleted);
      });
    });
};

const toggleTargetCompleted = (e) => {
  const target = e.currentTarget;
  const item = target.closest('.accordion-list__item');
  
  item.dataset.completed === 'true' ? item.dataset.completed = 'false' : item.dataset.completed = 'true';
  
  updateTarget(item)
    .then(() => {
      if (target.dataset.btn === 'done') {
        target.dataset.btn = 'refresh';
      } else {
        target.dataset.btn = 'done';
      }
    })
};

const fillForm = (e) => {
  showDeleteBtn()
  
  let input;
  const item = e.currentTarget.closest('.accordion-list__item');
  for (let d in item.dataset) {
    input = targetsForm.querySelector(`[name=${ d }]`);
    if (input) input.value = item.dataset[d];
  }
  
  addFormId(item.dataset.id);
  showDialog();
};

const closeForm = (e) => {
  e.preventDefault();
  removeErrorMsg();
  hideDeleteBtn()
  modalElement.close();
}

const addEntry = (e) => {
  e.preventDefault();
  
  showDialog();
  resetForm();
}

const sendForm = (e) => {
  e.preventDefault();
  
  const target = e.target;
  const formData = new FormData(targetsForm);
  
  
  if (validateForm(formData)) {
    if (targetsForm.dataset.formEntryId) {
      updateTarget(target)
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
    errorMsgElement.innerText = errorMessage;
  }
};

const deleteEntry = async (e) => {
  e.preventDefault();
  
  const formData = new FormData(targetsForm);
  const currentDate = getCurrentDate();
  activateLoader('delete');
  
  const api = createUrl(`/api/users/${ formData.get('user') }/target/${ currentDate }/${ targetsForm.dataset.entryId }/`);
  const res = await postData(api, {}, formData.get('csrfmiddlewaretoken'), 'DELETE');
  await showTargets();
  closeForm(e);
  deactivateLoader('Day target entry', 'delete');
};

const initHtmlElements = () => {
  addButtonElement = document.querySelector('[data-btn="target-add"]');
  modalElement = document.querySelector('[data-modal="targets"]');
  modalCloseButton = document.querySelector('form#targets [data-btn="close"]');
  targetsForm = document.querySelector('form#targets');
  errorMsgElement = document.querySelector('form#targets .error-msg');
  targetList = document.querySelector('[data-accordion-list="targets"]');
  deleteBtnElement = document.querySelector('[data-modal="targets"] [data-btn="delete"]');
};

const initEvents = () => {
  addButtonElement.addEventListener('click', addEntry);
  modalCloseButton.addEventListener('click', closeForm);
  targetsForm.addEventListener('submit', sendForm);
  deleteBtnElement.addEventListener('click', deleteEntry);
};

const init = () => {
  initHtmlElements();
  initEvents();
  showTargets();
};

init();