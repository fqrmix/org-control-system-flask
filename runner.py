from ocs import app, socketio
from ocs import views, websocket

if __name__ == '__main__':
    socketio.run(app, port=5050)