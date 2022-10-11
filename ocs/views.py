from ast import Pass
from flask import render_template, Response, jsonify
from ocs.models import Users, PassKeys
from ocs.cameramodule import main_camera, known_face_encodings_new, known_face_ids
from . import app


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

@app.route('/users')
def photoAll():
    users = Users.query.all()
    u = [user.__repr__() for user in users]
    return jsonify(meta = 'Success!', users = u)

@app.route('/pass_keys/<int:user_id>')
def pass_keys_all(user_id):
    pass_keys = PassKeys.query.filter_by(user_id = user_id).all()
    p = [pass_key.id for pass_key in pass_keys]
    u = [pass_key.user_id for pass_key in pass_keys]
    a = [pass_key.access_level for pass_key in pass_keys]
    return jsonify(meta = 'Success!', 
                pass_keys_ids = p,
                pass_keys_users = u,
                pass_keys_al = a
            )
