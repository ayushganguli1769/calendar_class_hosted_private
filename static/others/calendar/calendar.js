function get_colour_codes(percentage){//-> [backGroundColor, borderColor]
    let white = '#FFFFFF'
    let black = '#000000'
    let hardcorded_color_values = [
        ['#556B2F',white],//.dark olive gree
        ['#006400', white],//darkgreen
        ['#008000', white],//green
        ['#228B22', white],//forestgreen
        ['#3CB371', white],//mediumseagreen	
        ['#32CD32',black],//limegreen
        ['#00FF00',black],//lime	
        ['#ADFF2F',black],//greenyellow	
        ['#FFFF99',black],//lighyellow2
        ['#FFFF66',black],//lightyellow3
        ['#FFFF00',black],//yellow
        ['#f4ca16',black],//Jonquil
        ['#F9A602',black],//gold
        ['#FFA500',black],//orange
        ['#FF8C00',black],//darkorange
        ['#FF7F50',white],//coral
        ['#FF6347',white],//#tomato	
        ['#FF4500',white],//orangered	
        ['#FF0000',white],//red
        ['#DC143C',white],//crimson
        ['#B22222',white],//firebrick
        ['#8B0000',white],//darkred
        ['#800000',white],//maroon
    ]
    let index = Math.floor(percentage/5)
    return hardcorded_color_values[index]
}
function delete_task(curr_event){
    let curr_button = curr_event.target
    let curr_row = curr_button.parentElement.parentElement
    let curr_task_id = curr_button.getAttribute('data-taskid')
    alert(curr_task_id)
    let url = `/delete_task/${curr_task_id}/`
    fetch(url,{
        method:'POST',
        credentials: 'same-origin',
    }).then(
        response => response.json()
    ).then(
        data =>{
            if (data['is_success'] === true){
                curr_row.remove()
                console.log(data['message'])
            }
            else{
                console.log(data['message'])
            }
        }
    )
    
}
function show_tasks_for_day(event){
    let my_batch_name= document.getElementById("batch_name").value;
    let batch_code = document.querySelector("#list_batch_name"  + " option[value='" + my_batch_name+ "']").dataset.value;
    if (batch_code.length < 10){
        return
    }
    let curr_user_id = document.getElementById('user_id_hidden').value
    let curr_cell = event.target
    let day = parseInt(curr_cell.getAttribute('data-date') )
    let month = parseInt(curr_cell.getAttribute('data-month'))
    let year = parseInt(curr_cell.getAttribute('data-year'))
    console.log(day,month,year,'debug')
    let body_data = {
        'year': year,
        'month': month,
        'day': day,
        'batch_code': batch_code,
        'user_id': curr_user_id,
    }
    fetch('/get_all_tasks_on_day/',{
        method: "POST",
        headers: { "Content-Type": "application/json; charset=UTF-8" },
        body: JSON.stringify(body_data)
    }).then(
        response => response.json()
    ).then(
        data => {
            var table_rows_div = document.getElementById('task_particular_day_list_modal')
            table_rows_div.innerHTML = ``
            var myTbody = document.querySelector("#task_list_day_table_modal>tbody");
            for(let i=0; i < data['task_list'].length; i++){
                var newRow = myTbody.insertRow();
                console.log(data['stress_level'],'stress level on day due to tasks')
                newRow.insertCell().append(String(i+1));
                newRow.insertCell().append(data['task_list'][i].name);
                newRow.insertCell().append(data['task_list'][i].class_name);
                newRow.insertCell().append(data['task_list'][i].owner_faculty_name)
                var delete_button = document.createElement("BUTTON");
                delete_button.setAttribute('data-taskid',data['task_list'][i].task_id)
                if (data['task_list'][i].deletable === true){
                    delete_button.className = "btn btn-danger"
                    delete_button.textContent = "DELETE"
                    delete_button.addEventListener("click",(e)=> {delete_task(e)})
                }
                else{
                    delete_button.className = "btn btn-secondary disabled"
                    delete_button.textContent = "DISABLED"
                }
                newRow.insertCell().append(delete_button)
            }
            window.$('#staticBackdrop').modal('show');


        }
    )
}

function generate_year_range(start, end) {
    var years = "";
    for (var year = start; year <= end; year++) {
        years += "<option value='" + year + "'>" + year + "</option>";
    }
    return years;
}

today = new Date();
currentMonth = today.getMonth();
currentYear = today.getFullYear();
selectYear = document.getElementById("year");
selectMonth = document.getElementById("month");


createYear = generate_year_range(1970, 2050);
/** or
 * createYear = generate_year_range( 1970, currentYear );
 */

document.getElementById("year").innerHTML = createYear;

var calendar = document.getElementById("calendar");
var lang = calendar.getAttribute('data-lang');

var months = "";
var days = "";

var monthDefault = ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"];

var dayDefault = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"];

    months = monthDefault;
    days = dayDefault;

var $dataHead = "<tr>";
for (dhead in days) {
    //console.log(dhead,days)
    $dataHead += "<th data-days='" + days[dhead] + "'>" + days[dhead] + "</th>";
}
$dataHead += "</tr>";

//alert($dataHead);
document.getElementById("thead-month").innerHTML = $dataHead;


monthAndYear = document.getElementById("monthAndYear");
showCalendar(currentMonth, currentYear);



function next() {
    currentYear = (currentMonth === 11) ? currentYear + 1 : currentYear;
    currentMonth = (currentMonth + 1) % 12;
    showCalendar(currentMonth, currentYear);
}

function previous() {
    currentYear = (currentMonth === 0) ? currentYear - 1 : currentYear;
    currentMonth = (currentMonth === 0) ? 11 : currentMonth - 1;
    showCalendar(currentMonth, currentYear);
}

function jump() {
    currentYear = parseInt(selectYear.value);
    currentMonth = parseInt(selectMonth.value);
    showCalendar(currentMonth, currentYear);
}

function showCalendar(month, year) {

    var firstDay = ( new Date( year, month ) ).getDay() - 1;

    tbl = document.getElementById("calendar-body");

    let calendar_weight_dict = JSON.parse(localStorage.getItem('calendar_dict'))
    console.log(calendar_weight_dict,'weight_arr_retrieved')
    tbl.innerHTML = "";

    
    monthAndYear.innerHTML = months[month] + " " + year;
    selectYear.value = year;
    selectMonth.value = month;

    // creating all cells
    var date = 1;
    for ( var i = 0; i < 6; i++ ) {
        
        var row = document.createElement("tr");

        
        for ( var j = 0; j < 7; j++ ) {
            if ( i === 0 && j < firstDay ) {
                cell = document.createElement( "td" );
                cellText = document.createTextNode("");
                cell.appendChild(cellText);
                row.appendChild(cell);
            } else if (date > daysInMonth(month, year)) {
                break;
            } else {
                cell = document.createElement("td");
                //console.log(year,month+1,date)
                cell.setAttribute("data-date", date);
                cell.setAttribute("data-month", month + 1);
                cell.setAttribute("data-year", year);
                cell.setAttribute("data-month_name", months[month]);
                cell.className = "date-picker";
                var temp = cell.getAttribute('data-date')
                cell.addEventListener('click',(e)=>{
                    show_tasks_for_day(e)
                })
                let style_arr = null
                let curr_bg_color = null
                let curr_font_color = null
                let curr_date_string = `${String(year)}#${String(month+1)}#${String(date)}`
                if (curr_date_string in calendar_weight_dict){
                    style_arr = get_colour_codes(calendar_weight_dict[curr_date_string])
                    console.log(curr_date_string,style_arr)
                    curr_bg_color = style_arr[0]
                    curr_font_color = style_arr[1]
                    cell.style.background = curr_bg_color
                    cell.style.color = curr_font_color
                }
                //cell.style.background = '#FFA500'
                //cell.style.color = '#FFFFFF'
                cell.innerHTML = "<span>" + date + "</span>";

                if ( date === today.getDate() && year === today.getFullYear() && month === today.getMonth() ) {
                    cell.className = "date-picker selected";
                }
                row.appendChild(cell);
                date++;
            }


        }

        tbl.appendChild(row);
    }

}

function daysInMonth(iMonth, iYear) {
    return 32 - new Date(iYear, iMonth, 32).getDate();
}

function my_show_calendar_plan(curr_button){
    try{
        curr_button.disabled = true
        let my_batch_name= document.getElementById("batch_name").value;
        let batch_code = document.querySelector("#list_batch_name"  + " option[value='" + my_batch_name+ "']").dataset.value;
        let start_interval_string = document.getElementById('interval_start_date').value//month day year
        let end_interval_string = document.getElementById('interval_end_date').value//month day year
        let previous_days = document.getElementById('days_before').value
        let next_days = document.getElementById('days_after').value
        let curr_user_id = document.getElementById('user_id_hidden').value
        let alert_div = document.getElementById('alert_div_optimal_date_string')
        /*
        //hardcoding for now debug
        let batch_code = 'MYEHAOKDJG'
        let start_interval_string = '11/10/2022'
        let end_interval_string = '12/15/2022'
        let previous_days = '5'
        let next_days = '10'
        */
        let start_interval_arr = start_interval_string.split("/")
        let end_interval_arr = end_interval_string.split("/")
        let start_interval_year = start_interval_arr[2]
        let start_interval_month = start_interval_arr[0]
        let start_interval_day = start_interval_arr[1]
        let end_interval_year = end_interval_arr[2]
        let end_interval_month = end_interval_arr[0]
        let end_interval_day = end_interval_arr[1]
        let my_data = {
            'batch_code': batch_code,
            'start_interval_year': start_interval_year,
            'start_interval_month':start_interval_month,
            'start_interval_day': start_interval_day,
            'end_interval_year': end_interval_year,
            'end_interval_month': end_interval_month,
            'end_interval_day': end_interval_day,
            'previous_days':previous_days,
            'next_days': next_days,
            'user_id': curr_user_id,
        }
        //console.log(my_data)
        fetch('/show_calendar_plan/', {
            method: "POST",
            headers: { "Content-Type": "application/json; charset=UTF-8" },
            body: JSON.stringify(my_data)
        }
        
        ).then(
            response => response.json()
        ).then(
            data =>{
                alert_div.innerHTML = `
                <div class="alert alert-primary d-flex align-items-center mt-5 mb-2" role="alert">
                    <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" fill="currentColor" class="bi bi-exclamation-triangle-fill flex-shrink-0 me-2" viewBox="0 0 16 16" role="img" aria-label="Warning:">
                        <path d="M8.982 1.566a1.13 1.13 0 0 0-1.96 0L.165 13.233c-.457.778.091 1.767.98 1.767h13.713c.889 0 1.438-.99.98-1.767L8.982 1.566zM8 5c.535 0 .954.462.9.995l-.35 3.507a.552.552 0 0 1-1.1 0L7.1 5.995A.905.905 0 0 1 8 5zm.002 6a1 1 0 1 1 0 2 1 1 0 0 1 0-2z"/>
                    </svg>
                    <div>
                        The optimal date is ${data['optimal_day']}
                    </div>
                </div>
                `
                curr_button.disabled = false
                //console.log(data)
                let calendar_weight_dict = JSON.stringify(data['weight_dict'])
                localStorage.setItem( 'calendar_dict', calendar_weight_dict)
                localStorage.setItem('max_weight', data['maxi_val'] )
                let optimal_date = data['optimal_day']
                //console.log("the optimal date is ",optimal_date)
                currentMonth = parseInt(start_interval_month) -1
                currentYear = parseInt(start_interval_year)
                showCalendar(start_interval_month-1,start_interval_year)
            }
        ).catch(
            () =>{
                curr_button.disabled = false
                console.log("Something went wrong")
            }
        )
    }
    catch{
        console.log("Some value is missing. Please correct them")//show a div alert later
    }

}