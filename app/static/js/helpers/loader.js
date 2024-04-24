const activeCls = "active",
  alertCls = '.alert',
  alertTextCls = '.alert__notification';

const alertEl = document.querySelector(`${ alertCls }`),
  alertTextEl = document.querySelector(`${ alertTextCls }`);

const activateLoader = (operation) => {
  // create, update, delete
  let loadingText;
  switch (operation) {
    case 'create':
    case 'update':
      loadingText = "Saving...";
      break;
    case 'delete':
      loadingText = 'Deleting...';
      break;
    default:
      break;
  }
  
  alertTextEl.innerText = `${ loadingText }`;
  alertEl.classList.add(activeCls);
}

const deactivateLoader = (entryLabel, operation) => {
  alertTextEl.innerText = `${ entryLabel } ${operation}d.`;
  setTimeout(() => {
    alertEl.classList.remove(activeCls);
  }, 10000);
}

export { activateLoader, deactivateLoader };
