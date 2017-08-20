# -*- coding: utf-8 -*-
"""
    WhatAClass.app
    ~~~~~~~~~~~~~~~~~~~~~~

    Basic factory to initialize the app with its extensions.

    Loads blueprints and configuration, depending on which
    method you use it also initializes the db schema.

    :author: Javier Martínez
"""

from flask import Flask, request, session
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
    app = configure_app(app, config)
    app = initialize_extensions(app)
    expose_user_loader()
    app = register_blueprints(app)
    return app


def register_blueprints(app):
    """Register the blueprints to the app, this allows you to change the behaviour of the app
    depending on the instance, and which addons are added and which are not."""
    from .controllers import index, user_mng, tensorflow_mng, oauth_google
    app.register_blueprint(index)
    app.register_blueprint(user_mng)
    app.register_blueprint(oauth_google)
    if app.config['ADDONS']['TENSORFLOW'] is not False:
        # May be a string with True instead of the boolean True
        app.register_blueprint(tensorflow_mng)
    return app


def expose_user_loader():
    """Add the method that flask login needs to identify how users are going to be logged in."""
    from .models import User
    from .extensions import login_manager

    @login_manager.user_loader
    def load_user(user_id):
        """Method required by flask_login to identify how user are going to be logged in."""
        return User.query.filter(User.id == user_id.decode()).first()


def initialize_extensions(app):
    """Start the extensions that are going to be used in the app."""
    from .extensions import db, csrf, bcrypt, ts, babel, login_manager, oauth

    db.init_app(app)
    csrf.init_app(app)
    bcrypt.init_app(app)
    babel.init_app(app)
    login_manager.init_app(app)
    oauth.init_app(app)

    ts.secret_key = app.secret_key

    login_manager.login_view = 'user_mng.login'

    app = configure_babel(app, babel)

    app = configure_email_and_ssh(app)

    app = configure_oauth(app, oauth)

    return app


def configure_oauth(app, oauth):
    """Configure oauth. Only the google is added right now."""
    from .extensions import oauths

    google = oauth.remote_app(
        'google',
        consumer_key=app.config.get('GOOGLE_CLIENT_ID'),
        consumer_secret=app.config.get('GOOGLE_SECRET'),
        request_token_params={
            'scope': 'email'
        },
        base_url='https://www.googleapis.com/oauth2/v1/',
        request_token_url=None,
        access_token_method='POST',
        access_token_url='https://accounts.google.com/o/oauth2/token',
        authorize_url='https://accounts.google.com/o/oauth2/auth',
    )

    oauths['google'] = google

    @google.tokengetter
    def get_google_oauth_token():
        return session.get('google_token')

    return app


def configure_email_and_ssh(app):
    """Configure email and ssh, loading configuration from the configuration of the app."""
    from .util import email_server, ssh_config

    email_server.config = app.config['EMAIL_CONF']

    for key in app.config['SSH_CONF']:
        ssh_config[key] = app.config['SSH_CONF'][key]

    return app


def configure_babel(app, babel):
    """Configure babel with the languages that have been added and add the localization selector.
    In this case the localization selector checks for the best matches in the browser request."""
    from .extensions import LANGUAGES

    for key, value in app.config['LANGUAGES']:
        LANGUAGES[key] = value

    if babel.locale_selector_func is None:
        @babel.localeselector
        def get_locale():
            """Locale selector for babel."""
            return request.accept_languages.best_match(LANGUAGES.keys())

    return app


def configure_app(app, config):
    """Load default configuration, then modify it with the param configuration.
    The default configuration already depends on env variables to ease the configuration for different environments."""
    # Configuration
    app.config.from_object('config.default')
    config = dict() if config is None else config
    # Load argument config.
    for key, value in config:
        app.config[key] = value
    return app


def create_app_and_db(config=None):
    """"Factory that creates the app and creates all the tables with retries to give some time to the db to initialize,
    (up to 25 seconds). Does not recreate existing tables."""
    app = create_app(config)
    _create_all_tables(app)
    return app
