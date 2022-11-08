import hashlib
from ocs import socketio
from .cameramodule import main_camera
from .models import Users, PassKeys
from .units import OrganizationUnit, Main, get_current_unit
from .errors import (DoorError, UnknownUser, NotInside,
                    AccessError, IncorrectPassword, AlreadyInside)

@socketio.on('connect')
def handle_connect():
    print('User has connected')

@socketio.on('server')
def send_message(unit_type):
    unit = get_current_unit(unit_type)
    socketio.emit('update_dashboard_2', list(unit.get_state().values()))
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

@socketio.on('form_data_in')
def handle_form_in(client_data):
    try:
        current_user = Users.query.get(main_camera.current_id)
        unit = get_current_unit(client_data['unit'])
        if current_user is None:
            socketio.emit('update_log', f"[{client_data['unit']}] Unknown person trying to enter pin-code!")
            raise UnknownUser
        else:
            pass_key = PassKeys.query.filter_by(user_id = current_user.id).first()
            pass_key_hash = hashlib.md5(str(pass_key.pin_code).encode("utf-8")).hexdigest()
            if pass_key_hash == client_data['pin_code']:
                if unit.access_level > pass_key.access_level:
                    socketio.emit('update_log', f"[{client_data['unit']}] {current_user.username} trying to open door with not enough access level!")
                    raise AccessError
                else:
                    if unit.is_user_inside(current_user):
                        raise AlreadyInside
                    else:
                        unit.update_list(current_user, direction='in')
                        socketio.emit('update_log', f"[{client_data['unit']}] {current_user.username} entered correct pin-code!")
                        unit.door.open()
                        socketio.emit('update_dashboard_2', list(unit.get_state().values()))
            else:
                socketio.emit('update_log', f"[{client_data['unit']}] {current_user.username} entered incorrect pin-code!")
                raise IncorrectPassword

    except DoorError as error:
        socketio.emit('send_fail_message', error.reason)

@socketio.on('form_data_out')
def handle_form_out(client_data):
    try:
        current_user = Users.query.get(main_camera.current_id)
        unit = get_current_unit(client_data['unit'])
        if current_user is None:
            raise UnknownUser
        else:
            if not unit.is_user_inside(current_user):
                raise NotInside
            else:
                unit.door.open()
                unit.update_list(current_user, direction='out')
                socketio.emit('update_log', f"[{client_data['unit']}] {current_user.username} is out from room!")
                socketio.emit('update_dashboard_2', list(unit.get_state().values()))
    except DoorError as error:
        socketio.emit('send_fail_message', error.reason)

@socketio.on('disconnect')
def handle_close():
    print('User has disconnected')
