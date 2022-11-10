from . import database
from wtforms_alchemy import ModelForm, ModelFormField

class PassKeys(database.db.Model):
    """
        Модель для базы данных, содержащая информацию о пропусках.
            *id - ID пропуска;
            *access_level - Уровень доступа;
            *pin_code - Пин-код
    """
    id = database.db.Column(database.db.Integer, primary_key = True)
    access_level = database.db.Column(database.db.Integer, nullable=False)
    pin_code = database.db.Column(database.db.String(80), nullable=False)
    
    def __repr__(self) -> str:
        return f'<Pass {self.id}>'

class Users(database.db.Model):
    """
        Модель для базы данных, содержащая информацию о пользователях.
            *id - ID пользователя;
            *username - Имя пользователя;
            *role - Должнсть пользователя;
            *age - Возраст пользователя;
            *pass_key_id - ID пропуска, наследованный из класса PassKeys.
    """
    id = database.db.Column(database.db.Integer, primary_key = True)
    username = database.db.Column(database.db.String(80), nullable=False)
    role = database.db.Column(database.db.String(80), nullable=False)
    age = database.db.Column(database.db.Integer, nullable=False)
    pass_key_id = database.db.Column(database.db.Integer, database.db.ForeignKey(PassKeys.id))
    pass_key = database.db.relationship(PassKeys)

    def __repr__(self) -> str:
        return f'<User {self.username}>'


class PassKeysForm(ModelForm):
    class Meta:
        model = PassKeys

class UsersForm(ModelForm):
    class Meta:
        model = Users

    pass_key = ModelFormField(PassKeysForm)
