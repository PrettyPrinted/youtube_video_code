from flask import Flask 

from .extensions import db, celery_init_app
from .routes import main

from .models import Base

def create_app():
    app = Flask(__name__)
    app.config.from_prefixed_env()
    app.config["SQLALCHEMY_ENGINES"] = {"default": app.config["SQLALCHEMY_URI"]}
    app.config["CELERY"] = {"broker_url": app.config["REDIS_URL"], "result_backend": app.config["REDIS_URL"]}

    db.init_app(app)
    celery_init_app(app)

    app.register_blueprint(main)

    with app.app_context():
        Base.metadata.create_all(db.engine)
    return app