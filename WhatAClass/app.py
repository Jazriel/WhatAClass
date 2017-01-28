from flask import Flask
from flask_login import LoginManager
from itsdangerous import URLSafeTimedSerializer

def create_app():
    app = Flask(__name__, instance_relative_config=True)

    # Load instance specific configuration.
    app.config.from_pyfile('config.py')
    app.config.from_object('config.default')
    # Load configuration from env if it does not exist ignore it.
    app.config.from_envvar('WHATACLASS_CONFIG', silent=True)

    from .extensions import db, csrf, bcrypt, configure_ts_secret_key

    db.init_app(app)
    csrf.init_app(app)
    bcrypt.init_app(app)
    configure_ts_secret_key(app.config["SECRET_KEY"])

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

