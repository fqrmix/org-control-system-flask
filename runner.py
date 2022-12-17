from ocs import (views, websocket,
                app, socketio)

if __name__ == '__main__':
    socketio.run(app, port=5051)
