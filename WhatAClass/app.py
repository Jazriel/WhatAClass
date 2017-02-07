# -*- coding: utf-8 -*-
""""""# TODO document
from flask import Flask, request


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

    from .utils import email_server

    email_server.config = app.config['EMAIL_CONF']

    from .models import User

    from .controllers import index, user_mng, file_mng

    app.register_blueprint(index)
    app.register_blueprint(user_mng)
    app.register_blueprint(file_mng)

    return app

