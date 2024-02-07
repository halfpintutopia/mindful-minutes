// const fetchData = async (url = '') => {
// 	fetch(url)
// 		.then(async response => {
// 			return await response.json;
// 		})
// 		.catch(error => console.error('Error', error));
// };

const fetchData = async (url = '') => {
  try {
    const response = await fetch(url);
	  return await response.json();
  } catch (error) {
    console.error('Error', error);
  }
};

const postData = async (url = '', data = {}, token = '') => {
	return await fetch(url, {
		method: 'POST',
		headers: {
			'Content-Type': 'application/json',
			'X-CSRFToken': token
		},
		body: JSON.stringify(data)
	});
};

export {fetchData, postData};
