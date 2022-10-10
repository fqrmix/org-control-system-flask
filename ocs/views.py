from . import app
from ocs.cameramodule import main_camera, known_face_encodings_new, known_face_ids
from flask import render_template, Response


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
