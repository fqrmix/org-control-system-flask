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
    const socket = io.connect(`http://127.0.0.1:5051/`);
    socket.on('connect', function() {
        console.log('User has connected!');
        socket.emit('server', {unit_type: unit_type});
    });

    const user_name_element = document.getElementById("user_name")
    const age_element = document.getElementById("user_age")
    const access_level_element = document.getElementById("access_level")
    const user_role_element = document.getElementById("user_role")
    const pin_code_element = document.getElementById("user_pin_code")
    const log_window = document.getElementById("log_window")
    const log_messages_element = document.getElementById("log_messages")
    
    socket.on('update_dashboard_1', function(msg) {
        user_name_element.innerHTML = `Name: ${msg.current_name}`;
        age_element.innerHTML = `Age: ${msg.age}`;
        user_role_element.innerHTML = `Role: ${msg.role}`
        access_level_element.innerHTML = `Access level: ${msg.access_level}`;
        pin_code_element.innerHTML = `Pin code: ${msg.pin_code}`;
    });

    socket.on('update_dashboard_2', function(org_info) {
        console.log('update_dashboard_2')
        Object.keys(org_info).forEach(function(room){
            let current_dashboard_element = document.getElementById(room + "_dashboard2_info");
            current_dashboard_element.innerHTML = '';
            Object.values(org_info[room]).forEach(function(employee) {
                console.log(employee)
                const newLI = document.createElement('li');
                newLI.appendChild(
                    document.createTextNode(
                        `[In: ${employee.time_of_arrival}] ${employee.username}`
                    )
                );
                current_dashboard_element.appendChild(newLI);
            });
        });
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
        Ozone.fire('success', 'Дверь была успешно открыта!', "top-left")
    });

    socket.on('send_fail_message', function(error) {
        Ozone.fire('error', `Не удалось открыть дверь! Причина: ${error}`, "top-middle")
    });

    socket.on('door_closed_message', function (username) {
        Ozone.fire('success', 'Дверь была успешно закрыта!', "top-right")
    });
});
