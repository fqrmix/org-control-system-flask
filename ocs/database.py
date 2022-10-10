from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from .models import User
from ocs import app

db_name = 'users.db'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + db_name
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True

db = SQLAlchemy(app)

class Database:
    def __init__(self) -> None:
        self.session = None
        pass

    def create(self, db):
        try:
            db.create_all()
            self.session = db.session
        except Exception as error:
            print(error)

    def add(self, db, item, item_list=None):
        try:
            if self.session is not None:
                current_session = self.session
                if item_list is None:
                    db.current_session.add(item)
                else:
                    if type(item_list) != list:
                        raise TypeError("Type of item_list incorrect!"\
                            f"{type(item_list)} was presented.")
                    else:
                        for item in item_list:
                            db.current_session.add(item)
                    self.update(db)  
            else:
                raise Exception("Session isn't opened!")
        except Exception as error:
            print(error)

    
    def update(self, db):
        try:
            if self.session is not None:
                current_session = self.session
                db.current_session.commit()
            else:
                raise Exception("Session isn't opened!")
        except Exception as error:
            print(error)

users_list = list
admin = User(username='admin', access_level=6)
user = User(username='user', access_level=1)
users_list.append(admin, user)

Database.add(db=db, item_list=users_list)
