import hashlib
import datetime
from ocs import socketio
from .cameramodule import main_camera
from .models import Users, PassKeys
from .errors import (DoorOpeningError, UnknownUser,
                    AccessError, IncorrectPassword, AlreadyInside)

class AccessLevel:
    data = {
        'main_door': 0,
        'server_room_door': 6
    }

class OrganizationUnit:
    def __init__(self) -> None:
        self.employees_list = dict()

    def update_list(self, user) -> None:
        current_user = dict()
        current_user['username'] = user.username
        current_user['time_of_arrival'] = datetime.datetime.now().strftime("%H:%M:%S")
        self.employees_list[user.id] = current_user
        
    def get_state(self):
        return self.employees_list

    def is_user_inside(self, user):
        if user.id in self.employees_list:
            return True
        return False


my_organization = OrganizationUnit()

@socketio.on('connect')
def handle_connect():
    print('User has connected')
    socketio.emit('update_dashboard_2', list(my_organization.get_state().values()))

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
    try:
        current_user = Users.query.get(main_camera.current_id)
        if current_user is None:
            socketio.emit('update_log', f"[{client_data['door']}] Unknown person trying to enter pin-code!")
            raise UnknownUser
        else:
            pass_key = PassKeys.query.filter_by(user_id = current_user.id).first()
            pass_key_hash = hashlib.md5(str(pass_key.pin_code).encode("utf-8")).hexdigest()
            if pass_key_hash == client_data['pin_code']:
                if AccessLevel.data[client_data['door']] > pass_key.access_level:
                    socketio.emit('update_log', f"[{client_data['door']}] {current_user.username} trying to open door with not enough access level!")
                    raise AccessError
                else:
                    if my_organization.is_user_inside(current_user):
                        raise AlreadyInside
                    else:
                        my_organization.update_list(current_user)
                        socketio.emit('update_log', f"[{client_data['door']}] {current_user.username} entered correct pin-code!")
                        socketio.emit('send_success_message')
                        socketio.emit('update_dashboard_2', list(my_organization.get_state().values()))
            else:
                socketio.emit('update_log', f"[{client_data['door']}] {current_user.username} entered incorrect pin-code!")
                raise IncorrectPassword

    except DoorOpeningError as error:
        socketio.emit('send_fail_message', error.reason)

@socketio.on('disconnect')
def handle_close():
    print('User has disconnected')
