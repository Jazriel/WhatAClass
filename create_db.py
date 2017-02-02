# -*- coding: utf-8 -*-
""""""# TODO document
from WhatAClass.extensions import db
from WhatAClass.app import create_app
import os

if os.getenv('HEROKU') is not None:
    app = create_app('config.heroku')
else:
    app = create_app()

db.init_app(app)
db.create_all()

# TODO alembic
