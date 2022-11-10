from . import database

class Users(database.db.Model):
    id = database.db.Column(database.db.Integer, primary_key = True)
    username = database.db.Column(database.db.String(80))
    role = database.db.Column(database.db.String(80))
    age = database.db.Column(database.db.Integer)
    pass_key = database.db.relationship('PassKeys', backref='users', lazy=True)

    def __init__(self, username, age, role) -> None:
        self.username = username
        self.age = age
        self.role = role

    def __repr__(self) -> str:
        return f'<User {self.username}>'

class PassKeys(database.db.Model):
    id = database.db.Column(database.db.Integer, primary_key = True)
    user_id = database.db.Column(
        database.db.Integer,
        database.db.ForeignKey('users.id'),
        nullable=False)
    access_level = database.db.Column(database.db.Integer)
    pin_code = database.db.Column(database.db.String(80))
    
    def __init__(self, user_id, access_level, pin_code) -> None:
        self.user_id = user_id
        self.access_level = access_level
        self.pin_code = pin_code

    def __repr__(self) -> str:
        return f'<Pass {self.id} for user {self.user_id}>'


