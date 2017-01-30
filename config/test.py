"""Test config, import default, then modify."""
from .default import *

DEBUG = True

# : Instance variables

SQLALCHEMY_DATABASE_URI = 'sqlite:////created/in/test/runtime.db'

SECRET_KEY = 'This_key_is_not_a_secret'

EMAIL_CONF = {
    'FROM': None,
    'PASS': None,
    'HOST': None,
    'PORT': None,
}