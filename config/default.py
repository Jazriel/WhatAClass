# -*- coding: utf-8 -*-
"""Default configuration that should not change in normal circumstances."""
import os

SQLALCHEMY_TRACK_MODIFICATIONS = True
SQLALCHEMY_ECHO = False

BCRYPT_LOG_ROUNDS = 12

DEBUG = os.getenv('DEBUG', False)
INSTANCE = os.getenv('WAC_INSTANCE', False)

HEROKU = os.getenv('HEROKU', False)

LANGUAGES = {
    'en': 'English',
    'es': 'Español'
}

SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL', 'sqlite:////created/in/test/runtime.db')

SECRET_KEY = os.getenv('SECRET_KEY', 'This_key_is_not_a_secret')

EMAIL_CONF = {
    'FROM': os.getenv('EMAIL_FROM', None),
    'PASS': os.getenv('EMAIL_PASS', None),
    'HOST': os.getenv('EMAIL_HOST', None),
    'PORT': os.getenv('EMAIL_PORT', None),
}

