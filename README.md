# org-control-system-flask

## Project architecture
```
.
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
│   │   │   │   └── User3.jpg
│   │   │   ├── 4
│   │   │   │   ├── User4.jpg
│   │   │   │   └── User4-2.jpg
│   │   │   └── 5
│   │   │       └── User5.jpg
│   │   ├── __init__.py
│   │   ├── camera.py
│   │   └── face_enc
│   ├── web
│   │   ├── static
│   │   │   ├── css
│   │   │   │   └── main.css
│   │   │   └── js
│   │   │       └── /some_js_static
│   │   └── templates
│   │       └── index.html
│   ├── __init__.py                     ## App factory
│   ├── config.py
│   ├── database.py
│   ├── models.py
│   ├── views.py
│   └── websocket.py
├── config.py                           ## App config file
├── requirements.txt
├── runner.py                           ## Main runner
.
```
