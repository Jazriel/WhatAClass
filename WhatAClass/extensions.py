# -*- coding: utf-8 -*-
"""
    WhatAClass.extensions
    ~~~~~~~~~~~~~~~~~~~~~

    Extensions used by the app so that we don't reinvent the wheel.

    :author: Javier Martínez


"""
from flask_wtf import CSRFProtect
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from itsdangerous import URLSafeTimedSerializer
from flask_babel import Babel
from flask_login import LoginManager
from flask_oauthlib.client import OAuth


db = SQLAlchemy()
bcrypt = Bcrypt()
csrf = CSRFProtect()
babel = Babel()
login_manager = LoginManager()
ts = URLSafeTimedSerializer('NotSecretKey')  # TODO: MOVE TO CONFIG
LANGUAGES = dict()
oauth = OAuth()

oauths = {}