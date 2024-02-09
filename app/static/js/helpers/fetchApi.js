const fetchData = async (url = '') => {
  try {
    const response = await fetch(url);
	  return await response.json();
  } catch (error) {
    console.error('Error', error);
  }
};

const postData = async (url = '', data = {}, token = '', method = 'POST') => {
	return await fetch(url, {
		method: method,
		headers: {
			'Content-Type': 'application/json',
			'X-CSRFToken': token
		},
		body: JSON.stringify(data)
	});
};

export {fetchData, postData};
