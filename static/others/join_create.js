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
    let data_list = document.getElementById('list_batch_name')
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
            if (data['is_success'] === true){
                data_list.innerHTML += `
                <option data-value="${batch_code}" value="${data['batch_name']}">Batch Code:${batch_code}</option>
                `
            }

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

function create_batch(){
    let batch_name = document.getElementById('batch_name_main').value;
    let url = `/create_batch/${batch_name}/`
    button = document.getElementById('create_batch_button')
    button.disabled = true
    let data_list = document.getElementById('list_batch_name')
    fetch(url,{
        method:'POST',
        credentials: 'same-origin',
        headers: {
            "X-CSRFToken": getCookie("csrftoken")
        }
    } ).then(
        response => response.json()
    ).then(
        data =>{
            let alert_div = document.getElementById('alert_div_create_batch')
            button.disabled = false
            if ('is_success' in data && data['is_success'] === false){
                alert_div.innerHTML = `
                    <div class="alert alert-success alert-dismissible fade show" role="alert">
                        ${data['message']}
                        <button type="button" class="btn-close" data-bs-dismiss="alert" aria-label="Close"></button>
                    </div>
                    ` + alert_div.innerHTML 
                    return
            }
            alert_div.innerHTML = `
            <div class="alert alert-success alert-dismissible fade show" role="alert">
                Batch ${batch_name} created. <br> Teacher code :<strong> ${data['teacher_code']} </strong> Student Code :<strong> ${data['student_code']} </strong>
                <button type="button" class="btn-close" data-bs-dismiss="alert" aria-label="Close"></button>
            </div>
            ` + alert_div.innerHTML 
            data_list.innerHTML += `
            <option data-value="${data['teacher_code']}" value="${batch_name}">Batch Code:${data['teacher_code']}</option>
            `
        }
    ).catch(
        () =>{
            let alert_div = document.getElementById('alert_div_create_batch')
            button.disabled = false
            alert_div.innerHTML =  `
            <div class="alert alert-danger alert-dismissible fade show" role="alert">
                 Sorry, something went wrong! Please try again.
                <button type="button" class="btn-close" data-bs-dismiss="alert" aria-label="Close"></button>
            </div>
            ` + alert_div.innerHTML 
        }
    )
}

function create_class(){
    let class_name_val = document.getElementById('class_name_main').value
    let my_batch_name= document.getElementById("batch_name").value;
    let batch_data_set_val = document.querySelector("#list_batch_name"  + " option[value='" + my_batch_name+ "']").dataset.value;
    let list_batch_name_id= document.querySelector("#list_batch_name"  + " option[value='" + my_batch_name+ "']").dataset.id;
    let url = `/create_class/${batch_data_set_val}/${class_name_val}/`
    let button = document.getElementById('create_class_button')
    button.disabled = true
    fetch(url,{
            method:'POST',
            credentials: 'same-origin',
            headers: {
                "X-CSRFToken": getCookie("csrftoken")
            }
        }
        ).then(
            response => response.json()
        ).then(
            data =>{
                let alert_div = document.getElementById('alert_div_create_class')
                button.disabled = false
                if ('is_success' in data && data['is_success'] === false){
                    alert_div.innerHTML = `
                    <div class="alert alert-success alert-dismissible fade show" role="alert">
                        ${data['message']}
                    </div>
                    ` + alert_div.innerHTML
                    return
                }
                alert_div.innerHTML = `
                <div class="alert alert-success alert-dismissible fade show" role="alert">
                    Class ${data['class_name']} belonging to batch ${data['batch_name']} created. <br> 
                    Teacher's Class code :<strong> ${data['class_code']} </strong> <br>
                    Student's Class code :<strong> ${data['student_class_code']} </strong> <br>
                    <button type="button" class="btn-close" data-bs-dismiss="alert" aria-label="Close"></button>
                </div>
                ` + alert_div.innerHTML
            }
        ).catch(
            () =>{
                button.disabled = false
                let alert_div = document.getElementById('alert_div_create_class')
                alert_div.innerHTML = `
                    <div class="alert alert-danger alert-dismissible fade show" role="alert">
                        Unable to create class ${class_name_val}. Something went Wrong!
                        <button type="button" class="btn-close" data-bs-dismiss="alert" aria-label="Close"></button>
                    </div>
                    ` + alert_div.innerHTML
            }
        )
}

function join_class(){
    let class_code = document.getElementById('class_code_main').value
    let url = `/join_class_teacher/${class_code}/`
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