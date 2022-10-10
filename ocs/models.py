from flask_sqlalchemy import SQLAlchemy

model = SQLAlchemy.Model

class User(model):
    id = model.Column(model.Integer, primary_key = True)
    username = model.Column(model.String(80), unique=True)
    access_level = model.Column(model.Integer, unique=True)


    def __init__(self, username, access_level) -> None:
        self.username = username
        self.access_level = access_level

    def __repr__(self) -> str:
        return f'<User {self.username}>'