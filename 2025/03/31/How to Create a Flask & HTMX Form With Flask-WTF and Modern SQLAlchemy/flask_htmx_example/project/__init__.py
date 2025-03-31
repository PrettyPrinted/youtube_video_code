from flask import Flask

from .extensions import db
from .routes import main

def create_app():
    app = Flask(__name__)
    app.config['SQLALCHEMY_ENGINES'] = {"default": "sqlite:///db.sqlite3"}
    app.config["SECRET_KEY"] = "my-secret-key"
    db.init_app(app)

    app.register_blueprint(main)

    return app