# -*- coding: utf-8 -*-
"""
    tests.test_WhatAClass
    ~~~~~~~~~~~~~~~~~~~~~

    Tests for WhatAClass, fixtures will be placed in the
    tests file that they make sense to be in, if needed
    in more than one place they will be moved to a
    separate file fixture.py

    These tests are not tested to be run concurrently.
    With different environments it should work.


    :author: Javier Martínez


"""
import os
import tempfile
from pytest import fixture
from WhatAClass import create_app


@fixture
def app():
    """Test application."""
    _app = create_app('config.test')
    with _app.app_context() as context:
        yield _app
        return


@fixture
def db(app):
    """Test database."""
    fd, db_path = tempfile.mkstemp(suffix='.db')

    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + db_path

    from WhatAClass.extensions import db

    db.init_app(app)
    db.create_all()
    # TODO alembic apply migrations will go here
    yield db

    os.close(fd)
    os.unlink(db_path)


@fixture
def client(app, db):
    return app.test_client()

# TODO FIXIT
def sign_up(client, username, password):
    return client.post('/signup',
                       data=dict(username=username,
                                 password=password
                                 ),
                       follow_redirects=True)


def test_base(client):
    base = client.get('/')
    assert b'Welcome to this app.' in base.data


def test_signup(client):
    base = client.get('/signup')
    assert b'Sign up!' in base.data
    assert b'Email' in base.data
    assert b'Password' in base.data
    # TODO actually signup
