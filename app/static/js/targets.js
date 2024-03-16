import { compareOrder, getCurrentDate, removeAllInnerElements } from "./helpers/helpers.js";
import { fetchData, postData } from "./helpers/fetchApi.js";

const server = 'http://localhost:8008';

const errorMessage = `You haven't provided enough information, please fill in the form`;

let refreshButtonElement,
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
  const formData = new FormData(targetsForm);
  // console.log(data.dataset.completed === );
  formData.append("completed", data.dataset.completed === 'true' ? "True" : "False")
  const currentDate = getCurrentDate();
  
  // const dataObj = {};
  // for( let d in data.dataset) {
  //   console.log(34, d, data.dataset[d])
  //   dataObj[d] = data.dataset[d];
  // }
  
  const dataObj = createDataObject(formData);
  console.log(31, dataObj, formData, data.dataset.id)
  
  const api = `${ server }/api/users/${ formData.get('user') }/target/${ currentDate }/${ data.dataset.id }/`;
  console.log(api);
  await postData(api, dataObj, formData.get('csrfmiddlewaretoken'), 'PUT');
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
  targetsForm.dataset.id = id;
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
        // target.nextElementSibling.classList.add('done');
      } else {
        target.dataset.btn = 'done';
        // target.nextElementSibling.classList.remove('done');
      }
    })
};

const fillForm = (e) => {
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

const initHtmlElements = () => {
  addButtonElement = document.querySelector('[data-btn="target-add"]');
  modalElement = document.querySelector('[data-modal="targets"]');
  modalCloseButton = document.querySelector('form#targets [data-btn="close"]');
  targetsForm = document.querySelector('form#targets');
  errorMsgElement = document.querySelector('form#targets .error-msg');
  targetList = document.querySelector('[data-accordion-list="targets"]');
};

const initEvents = () => {
  addButtonElement.addEventListener('click', addEntry);
  modalCloseButton.addEventListener('click', closeForm);
  targetsForm.addEventListener('submit', sendForm);
};

const init = () => {
  initHtmlElements();
  initEvents();
  showTargets();
};

init();