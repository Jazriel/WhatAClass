# -*- coding: utf-8 -*-
""""""# TODO document
from WhatAClass.extensions import db
from WhatAClass.app import create_app

app = create_app()

db.init_app(app)
db.create_all()

# TODO alembic
