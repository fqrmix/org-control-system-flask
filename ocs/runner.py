from socket import socket
from unicodedata import name
from flask import Flask, render_template
from flask_socketio import SocketIO, emit

app = Flask(__name__,
            static_url_path='',
            static_folder='web/static',
            template_folder='web/templates')

socketio = SocketIO(app)

@app.route('/')
def index():
    return render_template('index.html')

@socket.on('my_event', namespace='/websocket')
def test_message(message):
    emit('my_response',
         {'data': 'test'})

if __name__ == '__main__':
    socketio.run(app)