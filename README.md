# Краткое описание
Проект, релизованный в рамках ВКР.
# Стэк
```
Flask
Flask-SocketIO
Flask-SQLAlchemy
Flask-WTF

Инструменты для классификации лиц:
face-recognition 1.3.0 (HOG + SVM [11])
opencv-python 4.6.0.66
dlib 19.24.0 
```
# Файловая структура проекта
```
├── instance
│   └── main.db
├── ocs
│   ├── cameramodule
│   │   ├── photos
│   │   │   ├── 1
│   │   │   │   └── User1.jpg
│   │   │   ├── 2
│   │   │   │   └── User2.jpg
│   │   │   ├── 3
│   │   │   │   ├── User3-1.jpg
│   │   │   │   ├── User3-2.jpg
│   │   │   │   └── User3-3.jpg
│   │   │   ├── 4
│   │   │   │   ├── User4-1.jpg
│   │   │   │   └── User4-2.jpg
│   │   │   ├── 5
│   │   │   │   └── User5.jpg
│   │   │   ├── 6
│   │   │   │   └── User6.jpg
│   │   │   └── 7
│   │   │       └── User7.jpg
│   │   ├── __init__.py
│   │   ├── camera.py
│   │   └── face_enc
│   ├── web
│   │   ├── static
│   │   │   ├── css
│   │   │   │   ├── fonts
│   │   │   │   │   └── Roboto-Light.ttf
│   │   │   │   ├── OzoneAlerts.css
│   │   │   │   └── main.css
│   │   │   └── js
│   │   │       ├── OzoneAlerts.js
│   │   │       └── websocket.js
│   │   └── templates
│   │       ├── accounting_room.html
│   │       ├── create.html
│   │       ├── index.html
│   │       └── server_room.html
│   ├── __init__.py
│   ├── database.py
│   ├── errors.py
│   ├── models.py
│   ├── socket.py
│   ├── units.py
│   ├── views.py
│   └── websocket.py
├── README.md
├── config.py
├── requirements.txt
├── run_server.sh
└── runner.py
```
# Схема взаимодействия компонентов в системе
![image](https://github.com/fqrmix/org-control-system-flask/assets/90894198/386b82ba-6020-48c6-a59f-61424dcea2a6)
# Схема взаимодействия backend'a и модуля camera.py
![image](https://github.com/fqrmix/org-control-system-flask/assets/90894198/2643c448-8a85-43a2-8a4e-6d5413e39c26)
