
function getCurrentTime() {
    const today = new Date();
    const date = today.getFullYear() + '-' + (today.getMonth() + 1) + '-' + today.getDate();
    const time = today.getHours() + ":" + today.getMinutes() + ":" + today.getSeconds();
    const dateTime = date + ' ' + time;
    return dateTime
}

// Hash md5 function
function hashCode(str) {
    return str.split('').reduce((prevHash, currVal) =>
        (((prevHash << 5) - prevHash) + currVal.charCodeAt(0))|0, 0);
}

// Updating fields
document.addEventListener("DOMContentLoaded", function() {
    const unit_type_p_element = document.getElementById("unit_type_p")
    unit_type_p_element.textContent += unit_type + ":"
    const socket = io.connect(`http://127.0.0.1:5051/`);
    socket.on('connect', function() {
        console.log('User has connected!');
        socket.emit('server', unit_type);
    });

    const user_name_element = document.getElementById("user_name")
    const age_element = document.getElementById("user_age")
    const access_level_element = document.getElementById("access_level")
    const pin_code_element = document.getElementById("user_pin_code")
    const log_window = document.getElementById("log_window")
    const log_messages_element = document.getElementById("log_messages")

    socket.on('update_dashboard_1', function(msg) {
        user_name_element.innerHTML = `Name: ${msg.current_name}`;
        age_element.innerHTML = `Age: ${msg.age}`;
        access_level_element.innerHTML = `Access level: ${msg.access_level}`;
        pin_code_element.innerHTML = `Pin code: ${msg.pin_code}`;
    });

    let employees_count = 0
    const organization_dashboard_element = document.getElementById("dashboard2_info");
    const organization_employees_count_element = document.getElementById("employees_count");
    socket.on('update_dashboard_2', function(employees_list) {
        employees_count = employees_list.length
        organization_dashboard_element.innerHTML = '';
        employees_list.forEach(function(employee) {
            const newLI = document.createElement('li');
            newLI.appendChild(document.createTextNode(`[In: ${employee.time_of_arrival}] ${employee.username}`));
            organization_dashboard_element.appendChild(newLI);
        });
        organization_employees_count_element.textContent = employees_count.toString();
    });

    socket.on('update_log', function(msg){
        let scroll_flag = false
        if (log_window.scrollHeight - log_window.scrollTop == log_window.offsetHeight) {
            scroll_flag = true
        }
        if (log_messages_element.childElementCount == 0) {
            const newLI = document.createElement('li');
            newLI.appendChild(document.createTextNode(`[${getCurrentTime()}] ${msg}`));
            log_messages_element.appendChild(newLI);
        } else {
            const lastChildMsg = log_messages_element.lastElementChild.innerHTML;
            if (!lastChildMsg.includes(msg)){
                const newLI = document.createElement('li');
                newLI.appendChild(document.createTextNode(`[${getCurrentTime()}] ${msg}`));
                log_messages_element.appendChild(newLI);
            }
        }
        if (scroll_flag) {
            log_window.scrollTop = log_window.scrollHeight;
        }
        
    });

    // Send pin code from data to server
    const pin_code_form_input = document.getElementById("pin_code_from")
    const pin_code_form_button = document.getElementById("pin_code_form_button")
    pin_code_form_button.onclick = async function (data) {
        data = {
            "pin_code": await hashwasm.md5(pin_code_form_input.value),
            "unit": unit_type
        }
        socket.emit('form_data_in', data);
    };
    const pin_code_form_out_button = document.getElementById("pin_code_form_out_button")
    pin_code_form_out_button.onclick = async function (data) {
        data = {
            "pin_code": await hashwasm.md5(pin_code_form_input.value),
            "unit": unit_type
        }
        socket.emit('form_data_out', data);
    };

    socket.on('send_success_message', function(username) {
        alert('Дверь была успешно открыта!')
    });

    socket.on('send_fail_message', function(error) {
        alert(`Не удалось открыть дверь! Причина: ${error}`)
    });

    socket.on('door_closed_message', function (username) {
        alert('Дверь была успешно закрыта')
    });
});