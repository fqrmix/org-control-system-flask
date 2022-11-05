import hashlib
from ocs import socketio
from .cameramodule import main_camera
from .models import Users, PassKeys

class Error:
    INCORRECT_PASSWORD = {
        'id': 0,
        'msg': 'Был введен неверный пин!'
    }
    UNKNOWN_PERSON = {
        'id': 1,
        'msg': 'На камере находится человек, незарегистрированный в организации!'
    }
    NOT_ENOUGH_ACCESS = {
        'id': 2,
        'msg': 'У пользователя недостаточный уровень доступа для открытия двери!'
    }

class AccessLevel:
    data = {
        'main_door': 0,
        'server_room_door': 6
    }
    


@socketio.on('connect')
def handle_connect():
    print('User has connected')

@socketio.on('server')
def send_message():
    while True:
        user = Users.query.get(main_camera.current_id)
        if user is not None:
            pass_key = PassKeys.query.filter_by(user_id = user.id).first()
            json_info = {
                    'current_name': user.username,
                    'age': user.age,
                    'access_level': pass_key.access_level,
                    'pin_code': pass_key.pin_code,
                }
            socketio.emit('update_log', f'{user.username} was on camera!')
            socketio.sleep(1)
        else:
            json_info = {
                    'current_name': 'Unknown',
                    'age': 0,
                    'access_level': 0,
                    'pin_code': 'None'
                }
        socketio.emit('update_dashboard_1', json_info)
        socketio.sleep(1)

@socketio.on('form_data')
def handle_form_input(client_data):
    current_user = Users.query.get(main_camera.current_id)
    if current_user is None:
        socketio.emit('update_log', f"[{client_data['door']}] Unknown person trying to enter pin-code!")
        socketio.emit('send_fail_message', Error.UNKNOWN_PERSON)
    else:
        pass_key = PassKeys.query.filter_by(user_id = current_user.id).first()
        pass_key_hash = hashlib.md5(str(pass_key.pin_code).encode("utf-8")).hexdigest()
        print('Backend: ', pass_key_hash)
        print('Frontend: ', client_data)
        if pass_key_hash == client_data['pin_code']:
            if AccessLevel.data[client_data['door']] > pass_key.access_level:
                socketio.emit('update_log', f"[{client_data['door']}] {current_user.username} trying to open door with not enough access level!")
                socketio.emit('send_fail_message', Error.NOT_ENOUGH_ACCESS)
            else:
                socketio.emit('update_log', f"[{client_data['door']}] {current_user.username} entered correct pin-code!")
                socketio.emit('send_success_message')
        else:
            socketio.emit('update_log', f"[{client_data['door']}] {current_user.username} entered incorrect pin-code!")
            socketio.emit('send_fail_message', Error.INCORRECT_PASSWORD)


@socketio.on('disconnect')
def handle_close():
    print('User has disconnected')
