#############################
######## APP Factory ########
#############################

from dotenv import load_dotenv
import os
from flask import Flask
from flask_socketio import SocketIO
from .database import db
from .models import Users, PassKeys


app = Flask(__name__,
            static_url_path='',
            static_folder='web/static',
            template_folder='web/templates')

load_dotenv()
app.config.from_object(os.environ['APP_SETTINGS'])

db.init_app(app)
with app.app_context():
    db.create_all()

socketio = SocketIO(app, cors_allowed_origins='*')
