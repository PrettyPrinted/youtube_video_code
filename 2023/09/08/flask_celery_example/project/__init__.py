import os

from flask import Flask

from .extensions import db
from .views import main
from .utils import make_celery

def create_app():
    app = Flask(__name__)
    
    app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get("DATABASE_URL")
    app.config["SECRET_KEY"] = "Oz8Z7Iu&DwoQK)g%*Wit2YpE#-46vy0n"
    app.config["CELERY_CONFIG"] = {"broker_url": os.environ.get("REDIS_URL"), "result_backend": os.environ.get("REDIS_URL")}

    db.init_app(app)

    celery = make_celery(app)
    celery.set_default()
    
    app.register_blueprint(main)

    return app, celery