from flask import Flask, render_template, Response
from flask_socketio import SocketIO, send, emit
from cameramodule.camera import Camera, known_face_encodings_new, known_face_ids
from utils.setinterval import Interval
import threading

app = Flask(__name__,
            static_url_path='',
            static_folder='web/static',
            template_folder='web/templates')

socketio = SocketIO(app, cors_allowed_origins='*')
main_camera = Camera()
interval = Interval()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/video_feed')
def video_feed():
    return Response(
        main_camera.connect(
            known_face_encodings=known_face_encodings_new,
            known_face_ids=known_face_ids,
            camera_id=1
        ), 
        mimetype='multipart/x-mixed-replace; boundary=frame')

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
    interval.stop_interval()

if __name__ == '__main__':
    socketio.run(app, port=5050)