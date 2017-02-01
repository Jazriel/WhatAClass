# -*- coding: utf-8 -*-
"""Test config, import default, then modify."""
from .default import *
import os

DEBUG = False

# : Instance variables

SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL', 'sqlite:////created/in/test/runtime.db')

SECRET_KEY = 'This_key_is_not_a_secret'

EMAIL_CONF = {
    'FROM': None,
    'PASS': None,
    'HOST': None,
    'PORT': None,
}