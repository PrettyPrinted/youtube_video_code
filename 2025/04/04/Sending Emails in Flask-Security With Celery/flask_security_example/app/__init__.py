from flask import Flask 
from flask_security import FSQLALiteUserDatastore

from .extensions import db, security, mail, celery_init_app
from .models import Role, User
from .routes import main
from .forms import ExtendedRegisterForm
from .utils import CeleryMailUtil

def create_app():
    app = Flask(__name__)

    app.config["SQLALCHEMY_ENGINES"] = {"default": "sqlite:///db.sqlite3"}
    app.config["SECRET_KEY"] = "mysecretkey"
    app.config["SECURITY_PASSWORD_SALT"] = "mysalt"
    app.config["SECURITY_REGISTERABLE"] = True
    app.config["SECURITY_SEND_REGISTER_EMAIL"] = True
    app.config["SECURITY_USE_REGISTER_V2"] = True

    app.config["SECURITY_RECOVERABLE"] = True
    app.config["SECURITY_CHANGEABLE"] = True
    app.config["SECURITY_CONFIRMABLE"] = True

    app.config["SECURITY_EMAIL_SENDER"] = "user@email.com"
    app.config["MAIL_SERVER"] = "smtp.email.com"
    app.config["MAIL_PORT"] = 587
    app.config["MAIL_USE_TLS"] = True
    app.config["MAIL_USERNAME"] = "user@email.com"
    app.config["MAIL_PASSWORD"] = "password"

    app.config["CELERY"] = {"broker_url": "redis://localhost:6379"}

    db.init_app(app)
    user_datastore = FSQLALiteUserDatastore(db, User, Role)
    security.init_app(app, user_datastore, register_form=ExtendedRegisterForm, mail_util_cls=CeleryMailUtil)
    mail.init_app(app)
    celery_init_app(app)

    app.register_blueprint(main)
    return app
