tinyMCE.init({
    mode : "specific_textareas",
    editor_selector : "mceEditor",   //<<<---- 
    height:"420"
});
function clear_class_name_list(){
    let class_name_data_list = document.getElementById('list_class_name')
    document.getElementById('class_name').value = ""
    document.getElementById('class_name').disabled = true
    class_name_data_list.innerHTML = ``
    let hidden_batch_code_html_elemnt = document.getElementById('batch_code_hidden')
    hidden_batch_code_html_elemnt.value = ""

}
function manage_batch_class_code(){//this function appends class names with class codes into list_class_names datalist
    try{
        let my_batch_name_div = document.getElementById("batch_name")
        let my_batch_name = my_batch_name_div.value
        let batch_code = document.querySelector("#list_batch_name"  + " option[value='" + my_batch_name+ "']").dataset.value;
        let hidden_batch_code_html_elemnt = document.getElementById('batch_code_hidden')
        hidden_batch_code_html_elemnt.value = batch_code
        if (batch_code.length < 10) {
            clear_class_name_list()
            return
        }
        let class_name_data_list = document.getElementById('list_class_name')
        let url = `/batch_class_list/${batch_code}/`
        fetch(url,{
            method:'POST',
            credentials: 'same-origin', 
        }).then(
            response => response.json()
        ).then(
            data =>{
                if ('is_success' in data && data['is_success'] === false){
                    clear_class_name_list()
                    return
                }
                document.getElementById('class_name').disabled = false
                let class_list_arr = data['all_classes_list']
                class_name_data_list.innerHTML = ``
                for(let i=0;i < class_list_arr.length;i++){
                    class_name_data_list.innerHTML += `
                        <option data-value="${class_list_arr[i].teacher_class_code}" value="${class_list_arr[i].class_name}">Batch Code:${class_list_arr[i].teacher_class_code}</option>
                    `
                }
            }
        ).catch(
            () =>{
                console.log("error")
                clear_class_name_list()
            }
        )    
    }
    catch{
        clear_class_name_list()
    }

}
function add_task_submit_event(curr_button){
    //write method to check if input is valid
    try{
        let my_class_name_div = document.getElementById("class_name")
        let my_class_name = my_class_name_div.value
        let class_code = document.querySelector("#list_class_name"  + " option[value='" + my_class_name+ "']").dataset.value;
        let hidden_description_content_input = document.getElementById('description_content_hidden')
        let description_value = tinyMCE.get('myTextArea').getContent()
        hidden_description_content_input.value = description_value
        let hidden_class_code_input = document.getElementById("class_code_hidden")
        hidden_class_code_input.value = class_code
        //user is being redirected so I am not enabling back the button.
        return true
    }
    catch(err){
        //write catch method later
        console.log(err)
        alert("Couldn't create please check your inputs")
        return false
    }

}