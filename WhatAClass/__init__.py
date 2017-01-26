# -*- coding: utf-8 -*-
"""
    WhatAClass
    ~~~~~

    Simple web app designed to be the GUI of another app.
    Provides users a simple way to upload files and request
    results.


"""

from flask import Flask
from flask_wtf import CSRFProtect
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager

app = Flask(__name__, instance_relative_config=True)

# Load instance specific configuration.
app.config.from_pyfile('config.py')
app.config.from_object('config.default')
# Load configuration from env if it does not exist ignore it.
app.config.from_envvar('APP_CONFIG_FILE', silent=True)

db = SQLAlchemy(app)

csrf = CSRFProtect(app)
bcrypt = Bcrypt(app)

from .models import User

from .controllers import index
from .controllers import user_mng

app.register_blueprint(index)
app.register_blueprint(user_mng)

login_manager = LoginManager(app=app)
login_manager.login_view = 'user_mng.login'


@login_manager.user_loader
def load_user(user_id):
    return User.query.filter(User.id == user_id).first()
