from flask import Flask
from flask_wtf.csrf import CSRFProtect
from .views.index import index
from .views.user_mng import user_mng

app = Flask(__name__, instance_relative_config=True)
csrf = CSRFProtect(app)

app.config.from_pyfile('config.py')

app.config.from_object('config.default')
# Load configuration from env if not exist ignore it.
app.config.from_envvar('APP_CONFIG_FILE', silent=True)

app.register_blueprint(index)
app.register_blueprint(user_mng)


