from ocs import socketio
from .cameramodule import main_camera

@socketio.on('connect')
def handle_connect():
    print('User has connected')

@socketio.on('server')
def sendmessage():
    while True:
        socketio.emit('update_current_id',
            {'current_id': main_camera.current_id})
        socketio.sleep(0.5)

@socketio.on('disconnect')
def handle_close():
    print('User has disconnected')
