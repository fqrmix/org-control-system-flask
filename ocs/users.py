from .models import Users, PassKeys
from .database import db
import hashlib

semen_user = Users(
    username='Semen Sergeev',
    age='23',
    role='System Admininstrator')
semen_pin = '123456'
db.session.add(semen_user)
semen_passkey = PassKeys(
    user_id=1,
    access_level=6,
    pin_code=hashlib.md5(semen_pin.encode("utf-8")).hexdigest())
db.session.add(semen_passkey)

egor_user = Users(
    username='Egor Mezhuev',
    age='23',
    role='Accounting Manager'
)
egor_pin = '654321'

db.session.add(egor_user)

egor_passkey = PassKeys(
    user_id=2,
    access_level=4,
    pin_code=hashlib.md5(egor_pin.encode("utf-8")).hexdigest()
)
db.session.add(egor_passkey)

vadim_user = Users(
    username='Vadim Maloman',
    age='24',
    role='Tech Support manager'
)
vadim_pin = '0987654321'

db.session.add(vadim_user)

vadim_passkey = PassKeys(
    user_id=3,
    access_level=2,
    pin_code=hashlib.md5(vadim_pin.encode("utf-8")).hexdigest()
)
db.session.add(vadim_passkey)

db.session.commit()
