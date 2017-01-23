from sqlalchemy.ext.hybrid import hybrid_property
from . import db, bcrypt


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    email = db.Column(db.String(64), unique=True)
    _password = db.Column(db.String(128))
    email_confirmed = db.Column(db.Boolean)
    is_active = db.Column(db.Boolean)

    def __init__(self, email, password, email_confirmed=False):
        self.email = email
        self.password = password
        self.email_confirmed = email_confirmed
        self.is_active = True

    @hybrid_property
    def password(self):
        return self._password

    @password.setter
    def _set_password(self, plaintext):
        self._password = bcrypt.generate_password_hash(plaintext)

    def is_correct_password(self, password):
        return bcrypt.check_password_hash(self.password, password)

    def __repr__(self):
        rep = ('User(email={}, password={}, confirmed={})'
               .format(self.email, self.password[0:9], self.email_confirmed))
        return rep

    def get_id(self):
        return self.id



