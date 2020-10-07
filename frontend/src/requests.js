const cashFlowEndpoint = '/demo/cash_flow'
const clientsEnpoint = '/demo/'

export const allClientsRequest = async() => {
  let res = await fetch(clientsEnpoint)
  return await res.json()
}

export const clientRequest = async(id) => {
  let res = await fetch(clientsEnpoint + id.toString())
  return await res.json()
}

export const cashFlowRequest = async() => {
  let res = await fetch(cashFlowEndpoint)
  return await res.json()
}

// Dates are a bit of a pain (because here they are ISO strings, date only).
// If I pass the string to the backend, then both back & front have strings.
// I will convert the date before passing it.
export const submitCashFlow = async(investment, newReturn, date) => {
  date = new Date(date)
  const config = {
    method: 'POST',
    headers: {
      'Accept': 'application/json',
      'Content-Type': 'application/json',
      'X-CSRFToken': getCookie('csrftoken'),
    },
    // Needed for django to accept csrf
    credentials: 'same-origin',
    body: JSON.stringify({
      investment_id: investment.id,
      return: newReturn,
      date: date.toISOString(),
    })
  }
  let res = await fetch(cashFlowEndpoint, config)
  return await res.json()
}

// CSRF & Django
// https://docs.djangoproject.com/en/3.1/ref/csrf/
function getCookie(name) {
  var cookieValue = null;
  if (document.cookie && document.cookie !== '') {
      var cookies = document.cookie.split(';');
      for (var i = 0; i < cookies.length; i++) {
          var cookie = cookies[i].trim();
          // Does this cookie string begin with the name we want?
          if (cookie.substring(0, name.length + 1) === (name + '=')) {
              cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
              break;
          }
      }
  }
  return cookieValue;
}