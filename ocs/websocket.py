import time
from flask import request
from ocs import socketio
from ocs.cameramodule import main_camera
from ocs.socket import socket_balancer
from ocs.models import Users, PassKeys
from ocs.units import get_current_unit, organization
from ocs.errors import *

@socketio.on('connect')
def handle_connect():
    socket_balancer.add_socket_connection(request.sid)
    print(socket_balancer.socket_list)
    print('User has connected')

@socketio.on('server')
def send_message(data):
    unit = get_current_unit(data['unit_type'])
    socketio.emit('update_dashboard_2', organization.get_state())
    if request.sid in socket_balancer.socket_list \
        and not socket_balancer.while_started:
        while True:
            socket_balancer.while_started = True
            user = Users.query.get(main_camera.current_id)
            if user is not None:
                pass_key = PassKeys.query.filter_by(id = user.pass_key_id).first()
                json_info = {
                        'current_name': user.username,
                        'age': user.age,
                        'role': user.role,
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
            time.sleep(1)

@socketio.on('form_data_in')
def handle_form_in(client_data):
    try:
        current_user = Users.query.get(main_camera.current_id)
        if current_user is None:
            socketio.emit(
                'update_log', 
                f"[{client_data['unit']}] "\
                f"Unknown person trying to enter pin-code!")
            raise UnknownUser
        
        pass_key = PassKeys.query.filter_by(
            id = current_user.pass_key_id).first()

        if pass_key.pin_code != client_data['pin_code']:
            socketio.emit(
                'update_log', 
                f"[{client_data['unit']}] {current_user.username} entered incorrect pin-code!")
            raise IncorrectPassword
            
        current_unit = get_current_unit(client_data['unit'])
        if current_unit.is_user_inside(current_user):
            raise AlreadyInside

        main_unit = get_current_unit('main_room')
        if current_unit is not main_unit:
            if not main_unit.is_user_inside(current_user):
                raise NotInsideMain

        if current_unit.access_level > pass_key.access_level:
            socketio.emit(
                'update_log', 
                f"[{client_data['unit']}] {current_user.username} "\
                f"trying to open door with not enough access level!")
            raise AccessError

        current_unit.update_list(current_user, direction='in')
        socketio.emit(
            'update_log', 
            f"[{client_data['unit']}] "\
            f"{current_user.username} entered correct pin-code!")
        current_unit.door.open()
        socketio.emit('update_dashboard_2', organization.get_state())
        current_unit.door.close()                       

    except DoorError as error:
        socketio.emit('send_fail_message', error.reason)

@socketio.on('form_data_out')
def handle_form_out(client_data):
    try:
        current_user = Users.query.get(main_camera.current_id)
        current_unit = get_current_unit(client_data['unit'])

        if current_user is None:
            raise UnknownUser

        if not current_unit.is_user_inside(current_user):
            raise NotInsideUnit

        current_unit.door.open()
        current_unit.update_list(current_user, direction='out')
        socketio.emit(
            'update_log', 
            f"[{client_data['unit']}] "\
            f"{current_user.username} is out from room!")
        socketio.emit('update_dashboard_2', organization.get_state())
        current_unit.door.close()
    except DoorError as error:
        socketio.emit('send_fail_message', error.reason)

@socketio.on('disconnect')
def handle_close():
    socket_balancer.popout_socket_connection(request.sid)
    print('User has disconnected')
    print(socket_balancer.socket_list)
