from flask import Flask 
from .utils import celery_init_app
from .views import main

def create_app():
    app = Flask(__name__)
    app.config.from_mapping(
        CELERY=dict(
            broker_url="redis://redis",
            result_backend="redis://redis",
        ),
    )

    app.register_blueprint(main)

    celery_init_app(app)

    return app