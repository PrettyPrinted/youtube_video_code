from flask import Flask 
from flask_security import FSQLALiteUserDatastore

from .extensions import db, security
from .models import Role, User
from .routes import main
from .forms import ExtendedRegisterForm

def create_app():
    app = Flask(__name__)

    app.config["SQLALCHEMY_ENGINES"] = {"default": "sqlite:///db.sqlite3"}
    app.config["SECRET_KEY"] = "mysecretkey"
    app.config["SECURITY_PASSWORD_SALT"] = "mysalt"
    app.config["SECURITY_REGISTERABLE"] = True
    app.config["SECURITY_SEND_REGISTER_EMAIL"] = False
    app.config["SECURIT_USE_REGISTER_V2"] = True

    app.config["SECURITY_RECOVERABLE"] = True
    app.config["SECURITY_CHANGEABLE"] = True
    app.config["SECURITY_CONFIRMABLE"] = False

    db.init_app(app)
    user_datastore = FSQLALiteUserDatastore(db, User, Role)
    security.init_app(app, user_datastore, register_form=ExtendedRegisterForm)

    app.register_blueprint(main)
    return app