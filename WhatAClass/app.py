# -*- coding: utf-8 -*-
""""""# TODO document
from flask import Flask, request


def create_app(config_file=None):
    """Factory that creates the app."""
    app = Flask(__name__, instance_relative_config=True)

    # Configuration
    app.config.from_object('config.default')
    # Load argument config.
    if config_file is not None:
        app.config.from_object(config_file)

    # TODO REDO move to env variables//Load instance specific configuration. Affected by config.
    if not app.config['HEROKU'] and not app.config['DEBUG']:
        app.config.from_pyfile('config.py')

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
        return User.query.filter(User.id == user_id).first()

    for key in app.config['LANGUAGES']:
        LANGUAGES[key] = app.config['LANGUAGES'][key]

    if babel.locale_selector_func is None:

        @babel.localeselector
        def get_locale():
            """Locale selector for babel."""
            return request.accept_languages.best_match(LANGUAGES.keys())

    from .utils import email_server

    email_server.config = app.config['EMAIL_CONF']

    from .models import User

    from .controllers import index, user_mng

    app.register_blueprint(index)
    app.register_blueprint(user_mng)

    return app

