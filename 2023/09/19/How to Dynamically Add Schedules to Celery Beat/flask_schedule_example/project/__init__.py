from flask import Flask

from .extensions import db
from .views import main
from .utils import make_celery

def create_app():
    app = Flask(__name__)
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///db.sqlite3"
    app.config["SECRET_KEY"] = "super-secret-key"
    app.config["CELERY_CONFIG"] = {"broker_url": "redis://localhost"}

    db.init_app(app)
    
    app.register_blueprint(main)

    celery = make_celery(app)
    celery.set_default()

    return app, celery