function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = jQuery.trim(cookies[i]);
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

function join_batch(){
    let batch_code = document.getElementById('batch_code_main').value;
    let url = `/join_batch/${batch_code}/`
    let button = document.getElementById('join_batch_button')
    button.disabled = true
    fetch(url,{
        method:'POST',
        credentials: 'same-origin',
        headers: {
            "X-CSRFToken": getCookie("csrftoken")
        } 
    }).then(
        response => response.json()
    ).then(
        data =>{
            //alert(JSON.stringify(data))
            button.disabled = false
            let alert_div = document.getElementById('alert_div_join_batch')
            alert_div.innerHTML =   `
                <div class="alert alert-success alert-dismissible fade show" role="alert">
                    ${data['message']} <br>
                    <button type="button" class="btn-close" data-bs-dismiss="alert" aria-label="Close"></button>
                </div>
            ` + alert_div.innerHTML 

            //batch_code is teachers batch code
        }
    ).catch(
        () =>{
            let alert_div = document.getElementById('alert_div_join_batch')
            button.disabled = false
            alert_div.innerHTML = `
            <div class="alert alert-danger alert-dismissible fade show" role="alert">
                <strong> Sorry, something went wrong! Please try again.
                <button type="button" class="btn-close" data-bs-dismiss="alert" aria-label="Close"></button>
            </div>
            ` + alert_div.innerHTML 
        }
    )
}

function join_class(){
    let class_code = document.getElementById('class_code_main').value
    let url = `/join_class_student/${class_code}/`
    let button = document.getElementById('join_class_button')
    button.disabled = true
    fetch(url,{
        method:'POST',
        credentials: 'same-origin',
        headers: {
            "X-CSRFToken": getCookie("csrftoken")
        }
    }).then(
        response => response.json()
    ).then(
        (data) =>{
            let alert_div = document.getElementById('alert_div_join_class')
            alert_div.innerHTML = `
                <div class="alert alert-success alert-dismissible fade show" role="alert">
                        ${data['message']}
                    <button type="button" class="btn-close" data-bs-dismiss="alert" aria-label="Close"></button>
                </div>
                ` + alert_div.innerHTML
            button.disabled = false
        }

    ).catch(
        ()=>{
            let alert_div = document.getElementById('alert_div_join_class')
            alert_div.innerHTML = `
                <div class="alert alert-danger alert-dismissible fade show" role="alert">
                    Something went wrong! Please try again later.
                    <button type="button" class="btn-close" data-bs-dismiss="alert" aria-label="Close"></button>
                </div>
                ` + alert_div.innerHTML
            button.disabled = false
        }
    )
}