import { authHeader } from "../_helpers";

export const vendingService = {
  buy,
};
function buy(productID, amount) {
  var data = {};
  data["amount"] = amount;
  data["rowID"] = productID;
  const requestOptions = {
    method: "POST",
    headers: authHeader(),
    body: JSON.stringify(data),
  };
  return fetch(`/api/buy`, requestOptions).then(handleResponse);
}

function handleResponse(response) {
  return response.text().then((text) => {
    const data = text && JSON.parse(text);
    if (!response.ok) {
      if (response.status === 401) {
        // auto logout if 401 response returned from api
        logout();
        location.reload(true);
      }

      const error = (data && data.message) || response.statusText;
      return Promise.reject(error);
    }

    return data;
  });
}
