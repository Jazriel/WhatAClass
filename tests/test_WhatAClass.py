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
from distutils.command.config import config

from pytest import fixture
from WhatAClass import create_app
from WhatAClass.models import User


confirmed_user = dict(email='jmr@ubu.es',
                      password='pw')

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
    user = User(confirmed_user['email'], confirmed_user['password'], email_confirmed=True)
    db.session.add(user)
    db.session.commit()
    # TODO alembic apply migrations will go here
    yield db

    os.close(fd)
    os.unlink(db_path)


@fixture
def client(app, db):
    return app.test_client()


def get_csrf_token_from_data(data):
    pre = b'name="csrf_token" type="hidden" value="'
    index = data.find(pre)
    return data[index+len(pre):].split(b'"')[0]


# TODO FIXIT
def sign_up(client, email, password):
    page = client.get('/signup')
    return client.post('/signup',
                       data=dict(email=email,
                                 password=password,
                                 csrf_token=get_csrf_token_from_data(page.data)
                                 ),
                       follow_redirects=True)


def login(client, email, password):
    page = client.get('/login')
    return client.post('/login',
                       data=dict(email=email,
                                 password=password,
                                 csrf_token=get_csrf_token_from_data(page.data)
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
    base = sign_up(client, 'javyermartinez@gmail.com', '1234')
    assert b'Signed up successfully.' in base.data


def test_non_conf_email_login(client):
    em = 'javyermartinez@gmail.com'
    ps = '1234'
    sign_up(client, em, ps)
    page = login(client, em, ps)
    assert b'Email was not confirmed yet.' in page.data


def test_login(client):
    page = login(client, confirmed_user['email'], confirmed_user['password'])
    assert b'Logged in successfully.' in page.data


