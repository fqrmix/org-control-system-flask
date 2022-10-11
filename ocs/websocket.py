from ast import Pass
from ocs import socketio
from .cameramodule import main_camera
from .models import Users, PassKeys

@socketio.on('connect')
def handle_connect():
    print('User has connected')

@socketio.on('server')
def sendmessage():
    while True:
        user = Users.query.get(main_camera.current_id)
        if user is not None:
            pass_key = PassKeys.query.filter_by(user_id = user.id).first()
            json_info = {
                    'current_name': user.username,
                    'age': user.age,
                    'access_level': pass_key.access_level,
                    'pin_code': pass_key.pin_code
                }
        else:
            json_info = {
                    'current_name': 'Unknown',
                    'age': 0,
                    'access_level': 0,
                    'pin_code': 'None'
                }
        socketio.emit('update_dashboard_1', json_info)
        socketio.sleep(0.5)

@socketio.on('disconnect')
def handle_close():
    print('User has disconnected')
