from flask import Flask

from .extensions import db
from .views import main
from .utils import make_celery

from celery.schedules import crontab

def create_app():
    app = Flask(__name__)
    
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///db.sqlite3"
    app.config["SECRET_KEY"] = "Oz8Z7Iu&DwoQK)g%*Wit2YpE#-46vy0n"
    app.config["CELERY_CONFIG"] = {"broker_url": "redis://redis", "result_backend": "redis://redis", "beat_schedule": {
        "every-20-seconds" : {
            "task": "project.tasks.twenty_seconds",
            "schedule": crontab(hour=2, minute=25, day_of_week=2),
            #"args": (1, 2)
        }
    }}

    db.init_app(app)

    celery = make_celery(app)
    celery.set_default()
    
    app.register_blueprint(main)

    return app, celery