from flask import Flask 

from app.extensions import db
from app.routes import main

def create_app():
    app = Flask(__name__)
    app.config.from_prefixed_env()

    db.init_app(app)

    app.register_blueprint(main)

    return app
    