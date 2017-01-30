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

db = SQLAlchemy()
bcrypt = Bcrypt()
csrf = CSRFProtect()
ts = URLSafeTimedSerializer('NotSecretKey')
