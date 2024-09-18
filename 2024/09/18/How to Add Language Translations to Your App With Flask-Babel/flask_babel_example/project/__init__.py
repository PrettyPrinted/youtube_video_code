from flask import Flask 

from .extensions import db, babel, get_locale
from .routes import main

def create_app():
    app = Flask(__name__)
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///db.sqlite3"
    app.config["BABEL_TRANSLATION_DIRECTORIES"] = "/home/anthony/flask_babel_example/translations"
    
    db.init_app(app)
    babel.init_app(app, locale_selector=get_locale)

    app.register_blueprint(main)

    return app