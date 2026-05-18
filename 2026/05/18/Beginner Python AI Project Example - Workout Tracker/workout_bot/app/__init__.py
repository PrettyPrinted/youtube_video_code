from flask import Flask

from .extensions import celery_init_app, db
from .routes import main
from .utils import setup_llm_telemetry

def create_app():
    app = Flask(__name__)

    app.config.from_prefixed_env()

    setup_llm_telemetry(app)

    db.init_app(app)
    celery_init_app(app)

    app.register_blueprint(main)

    return app