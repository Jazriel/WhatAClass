# -*- coding: utf-8 -*-
"""
    WhatAClass.models
    ~~~~~~~~~~~~~~~~~

    The usual web-app architecture is the MVC
    (Model-View-Controller). This class implements
    the models of the architecture.

    :author: Javier Martínez


"""
from sqlalchemy.ext.hybrid import hybrid_property
from .extensions import db, bcrypt


class User(db.Model):
    """User class, implemented with the help of SQLalchemy to be persistent.
    Basically has a id and an email both unique, a password, a field to know
    if the password has been confirmed and the is_active field needed by flask.
    """
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    email = db.Column(db.String(64), unique=True)
    _password = db.Column(db.String(128))
    email_confirmed = db.Column(db.Boolean)

    def __init__(self, email, password, email_confirmed=False):
        self.email = email
        self.password = password
        self.email_confirmed = email_confirmed

    @hybrid_property
    def password(self):
        """Hybrid property to auto-encrypt the password at the setter."""
        return self._password

    @password.setter
    def password(self, plaintext):
        """Part of the hybrid property pattern. Modified setter
        to auto-encrypt."""
        self._password = bcrypt.generate_password_hash(plaintext)

    def is_correct_password(self, password):
        """Returns the check to ensure the passwords are the same."""
        return bcrypt.check_password_hash(self.password, password)

    def __repr__(self):
        """Representation of User."""
        rep = ('User(email={}, password={}, confirmed={})'
               .format(self.email, self.password[0:9], self.email_confirmed))
        return rep

    def get_id(self):
        """Get id method used by flask's login system."""
        return self.id

    @property
    def is_authenticated(self):
        return True

    @property
    def is_active(self):
        return True

    @property
    def is_anonymous(self):
        return False
