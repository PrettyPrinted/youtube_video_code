from flask import Flask 

from .extensions import db, celery_init_app
from .routes import main

def create_app():
    app = Flask(__name__)
    app.config["SQLALCHEMY_ENGINES"] = {"default": "sqlite:///db.sqlite3"}
    app.config["CELERY"] = {"broker_url": "redis://localhost:6379", "result_backend": "redis://localhost:6379"}

    db.init_app(app)
    celery_init_app(app)

    app.register_blueprint(main)
    return app