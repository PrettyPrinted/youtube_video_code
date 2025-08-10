from flask import Flask 
from .extensions import db, alembic

def create_app():
    app = Flask(__name__)
    app.config["SQLALCHEMY_ENGINES"] = {"default": "sqlite:///db.sqlite3"}
    app.config["ALEMBIC_CONTEXT"] = {"render_as_batch": True}

    db.init_app(app)
    alembic.init_app(app)

    return app