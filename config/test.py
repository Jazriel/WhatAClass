"""Test config, import default, then modify."""
from .default import *

DEBUG=True

# : Override instance variables

SECRET_KEY= 'This_key_is_not_a_secret'
EMAIL_PASS = 'None'