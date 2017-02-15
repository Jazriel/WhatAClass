# -*- coding: utf-8 -*-
""""""# TODO document
from WhatAClass.extensions import db
from WhatAClass.app import create_app

app = create_app()

with app.app_context():
    db.init_app(app)
    db.drop_all()
    db.create_all()

# TODO alembic
