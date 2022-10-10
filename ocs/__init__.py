#############################
######## APP Factory ########
#############################


import os
from flask import Flask
from flask_socketio import SocketIO


app = Flask(__name__,
            static_url_path='',
            static_folder='web/static',
            template_folder='web/templates')

app.config.from_object(os.environ['APP_SETTINGS'])

socketio = SocketIO(app, cors_allowed_origins='*')

