# -*- coding: utf-8 -*-
"""Default configuration that should not change in normal circumstances."""
import os

# SQLALCHEMY
SQLALCHEMY_TRACK_MODIFICATIONS = True
SQLALCHEMY_ECHO = False
SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL', 'sqlite:////var/lib/whataclass/user_db.db')

# BCRYPT
BCRYPT_LOG_ROUNDS = 12


DEBUG = os.getenv('DEBUG', False)

HEROKU = os.getenv('HEROKU', False)  # TODO Stop suporting heroku

# Internationalization
LANGUAGES = {
    'en': 'English',
    'es': 'Español'
}

SECRET_KEY = os.getenv('SECRET_KEY', 'This_key_is_not_a_secret')

GOOGLE_CLIENT_ID = os.getenv('GOOGLE_CLIENT_ID',  '1053761769020-93r9rhndvmp6ln89n3a644nmsbs8mrl9.apps.googleusercontent.com')

GOOGLE_SECRET = os.getenv('GOOGLE_SECRET', '3o8PiPk3EE33u6ribuLVsssV')


EMAIL_CONF = {
    'FROM': os.getenv('EMAIL_FROM', None),
    'PASS': os.getenv('EMAIL_PASS', None),
    'HOST': os.getenv('EMAIL_HOST', None),
    'PORT': os.getenv('EMAIL_PORT', 0),
}

SSH_CONF = {
    'HOST': os.getenv('WORKER_HOST_NAME', 'worker'),
    'PORT': os.getenv('WORKER_PORT', 22),
    'USER': os.getenv('WORKER_USER', 'root'),
    'PASS': os.getenv('WORKER_PASSWORD', 'screencast'),
}



ADDONS = {
    'TENSORFLOW': os.getenv('TENSORFLOW', False),
    # Add optional displays depending on deploy
}

