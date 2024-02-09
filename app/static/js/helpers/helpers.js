const padToDigits = (num) => {
	return num.toString().padStart(2, '0');
};

const getCurrentDate = () => {
	const currentDate = new Date(Date.now());
	// https://bobbyhadz.com/blog/javascript-format-date-yyyymmdd
	return [
		currentDate.getFullYear(),
		padToDigits(currentDate.getMonth() + 1),
		padToDigits(currentDate.getDate())
	].join('-');
};

const compareOrder = (a, b) => {
	return a.order - b.order;
};

const removeAllInnerElements = (element) => {
	let child = element.lastElementChild;
	while (child) {
		element.removeChild(child);
		child = element.lastElementChild;
	}
};

export { getCurrentDate, compareOrder, removeAllInnerElements };
