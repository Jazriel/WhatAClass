from flask import Flask
from flask_login import LoginManager


def create_app(config=None):
    """Factory that creates the app."""
    app = Flask(__name__, instance_relative_config=True)

    # Load instance specific configuration.
    app.config.from_pyfile('config.py')
    app.config.from_object('config.default')
    # Load argument config.
    if config is not None:
        app.config.from_object(config)

    # Load configuration from env if it does not exist ignore it.
    app.config.from_envvar('WHATACLASS_CONFIG', silent=True)

    from .extensions import db, csrf, bcrypt, ts

    db.init_app(app)
    csrf.init_app(app)
    bcrypt.init_app(app)
    ts.secret_key = app.secret_key

    from .utils import email_server

    email_server.config = app.config['EMAIL_CONF']

    from .models import User

    from .controllers import index, user_mng

    app.register_blueprint(index)
    app.register_blueprint(user_mng)

    login_manager = LoginManager(app=app)
    login_manager.login_view = 'user_mng.login'

    @login_manager.user_loader
    def load_user(user_id):
        """Method required by flask to identify how user are going to be logged in."""
        return User.query.filter(User.id == user_id).first()

    return app

