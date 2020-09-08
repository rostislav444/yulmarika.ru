const csrf = Cookies.get()

function XHR(method, url, data) {
    let request = new XMLHttpRequest();
        request.open(method, url, false);
        request.setRequestHeader("dataType", "json")
        request.setRequestHeader("Content-Type", "application/json");
        request.setRequestHeader("X-CSRFToken", csrf["csrftoken"]);
        request.send(data)
        if (request.status == 200) {
             return JSON.parse(request.responseText);
        } else if (request.status == 403) {
            document.location.reload(true);
        } else {
            alert('Ошибка: ' + request.status)
        }

}


function xhrOnLoad(method, url, data, func, field=undefined) {
    let request = new XMLHttpRequest();
        request.open(method, url, true);
        request.setRequestHeader("dataType", "json")
        request.setRequestHeader("Content-Type", "application/json");
        request.setRequestHeader("X-CSRFToken", csrf["csrftoken"]);
        request.send(data)
        request.onload = () => {
            func(request.responseText, field)
        }
}


