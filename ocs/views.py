from flask import request, render_template, Response, jsonify
from ocs.models import Users, PassKeys, UsersForm
from ocs.cameramodule import main_camera, known_face_encodings_new, known_face_ids
from . import app, db
import hashlib


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/server_room/')
def server():
    return render_template('server_room.html')

@app.route('/accounting_room/')
def accounting():
    return render_template('accounting_room.html')

@app.route('/video_feed')
def video_feed():
    return Response(
        main_camera.connect(
            known_face_encodings=known_face_encodings_new,
            known_face_ids=known_face_ids,
            camera_id=1
        ), 
        mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route("/create_user/", methods=["GET", "POST"])
def create_user():
    form = UsersForm(request.form)
    success = False
    if request.method == "POST":
        if form.validate():
            user = Users(
                username=form.username.data,
                age=form.age.data,
                role=form.role.data
            )
            pin = form.pass_key.pin_code.data
            form.pass_key.pin_code.data = hashlib.md5(pin.encode("utf-8")).hexdigest()
            form.populate_obj(user)
            db.session.add(user)
            db.session.commit()
            success = True

    return render_template("create.html", form=form, success=success)


@app.route('/users/')
def users():
    users = Users.query.all()
    u = [f'{user.__repr__()} with ID: {user.id}' for user in users]
    return jsonify(meta = 'Success!', users = u)


@app.route('/users/<int:user_id>')
def users_by_id(user_id):
    users = Users.query.filter_by(id = user_id).first()
    user_data = {
        'id': users.id,
        'username': users.username,
        'role': users.role,
        'pass_key_id': users.pass_key_id
    }
    current_pass_key = PassKeys.query.filter_by(id = users.pass_key_id).first()
    pass_key_data = {
        'pass_key_id': current_pass_key.id,
        'access_level': current_pass_key.access_level,
        'pin_code_hash': current_pass_key.pin_code
    }
    return jsonify(meta = 'Success!', pass_key_data=pass_key_data, user_data = user_data)

@app.route('/pass_keys')
def pass_keys():
    pass_keys = PassKeys.query.all()
    u = [f'{key.__repr__()} with ID: {key.id}' for key in pass_keys]
    return jsonify(meta = 'Success!', pass_keys = u)

@app.route('/pass_keys/<int:pass_key_id>')
def pass_keys_by_id(pass_key_id):
    pass_key = PassKeys.query.filter_by(id = pass_key_id).first()
    id = pass_key.id
    pin = pass_key.pin_code
    level = pass_key.access_level
    return jsonify(
                id = id,
                pin_code_hash = pin,
                access_level = level
            )
