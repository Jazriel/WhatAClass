# -*- coding: utf-8 -*-
"""
    tests.test_WhatAClass
    ~~~~~~~~~~~~~~~~~~~~~

    Tests for WhatAClass, fixtures will be placed in the
    tests file that they make sense to be in, if needed
    in more than one place they will be moved to a
    separate file fixture.py


    :author: Javier Martínez


"""
import os
import tempfile
from pytest import fixture
from WhatAClass import create_app

@fixture
def _app(self):
    """Test application."""
    if self._s_app is None:
        self._s_app = create_app('config.test')
    # with self._s_app.te
    # return

@fixture
def db(app):
    """Test database."""
    fd, db_path = tempfile.mkstemp(suffix='.db')
    if os.path.exists(db_path):
        os.unlink(db_path)

    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + db_path

    from WhatAClass.extensions import db
    db.init_app(app)
    db.create_all()
    # alembic apply migrations will go here
    yield db

    os.close(fd)
    os.unlink(db_path)


@fixture
def app(app, db):

    return app.test_client()

def test_base(app):
    # app.get
    pass


