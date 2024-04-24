const activeCls = "active",
  alertCls = '.alert',
  alertTextCls = '.alert__notification';

const alertEl = document.querySelector(`${ alertCls }`),
  alertTextEl = document.querySelector(`${ alertTextCls }`);

const activateLoader = () => {
  const savingTxt = "Saving...";
  alertTextEl.innerText = `${ savingTxt }`;
  alertEl.classList.add(activeCls);
}

const deactivateLoader = (entryLabel) => {
  alertTextEl.innerText = `${ entryLabel } saved.`;
  setTimeout(() => {
    alertEl.classList.remove(activeCls);
  }, 5000);
}

export { activateLoader, deactivateLoader };
