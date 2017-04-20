# -*- coding: utf-8 -*-
"""
    WhatAClass.app
    ~~~~~~~~~~~~~~~~~~~~~~

    Basic factory to initialize the app with its extensions.

    Loads blueprints and configuration, depending on which
    method you use it also initializes the db schema.

    :author: Javier Martínez
"""

from flask import Flask, request
from WhatAClass.extensions import db


def _create_all_tables(app):
    """Creates all the tables with retries to give some time to the db to initialize,
    does not recreate existing tables."""
    print('Trying to create tables')
    max_attemps = 5
    with app.app_context():
        for n in range(max_attemps):
            try:
                db.init_app(app)
                db.create_all()
            except Exception as e:
                print('Attempt failed ({}/{}): {}'.format(n+1, max_attemps, e))
                from time import sleep
                sleep(5)
                # Could not create db: failing
                if n+1 == max_attemps:
                    print('Could not create db')
                    raise
            else:
                print('Finished creating tables')
                return


def create_app(config=None):
    """Factory that creates the app."""
    app = Flask(__name__, instance_relative_config=True)

    # Configuration
    app.config.from_object('config.default')

    if app.config['INSTANCE']:
        app.config.from_pyfile('config.py')

    config = dict() if config is None else config
    # Load argument config.
    for key, value in config:
        app.config[key] = value

    from .extensions import db, csrf, bcrypt, ts, babel, login_manager, LANGUAGES

    db.init_app(app)
    csrf.init_app(app)
    bcrypt.init_app(app)
    babel.init_app(app)
    login_manager.init_app(app)
    ts.secret_key = app.secret_key

    login_manager.login_view = 'user_mng.login'

    @login_manager.user_loader
    def load_user(user_id):
        """Method required by flask_login to identify how user are going to be logged in."""

        return User.query.filter(User.id == user_id.decode()).first()

    for key, value in app.config['LANGUAGES']:
        LANGUAGES[key] = value

    if babel.locale_selector_func is None:
        @babel.localeselector
        def get_locale():
            """Locale selector for babel."""
            return request.accept_languages.best_match(LANGUAGES.keys())

    from .util import email_server, ssh_config

    email_server.config = app.config['EMAIL_CONF']

    for key in app.config['SSH_CONF']:
        ssh_config[key] = app.config['SSH_CONF'][key]

    from .models import User

    from .controllers import index, user_mng, neuralnet_mng

    app.register_blueprint(index)
    app.register_blueprint(user_mng)
    app.register_blueprint(neuralnet_mng)

    return app


def create_app_and_db(config=None):
    """"Factory that creates the app and creates all the tables with retries to give some time to the db to initialize,
    (up to 25 seconds). Does not recreate existing tables."""
    app = create_app(config)
    _create_all_tables(app)
    return app
