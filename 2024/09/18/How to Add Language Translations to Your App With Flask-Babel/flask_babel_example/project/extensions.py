from flask import request
from flask_sqlalchemy import SQLAlchemy
from flask_babel import Babel

def get_locale():
    language = request.accept_languages.best_match(["en", "es"])
    print("Selected Language", language)
    return language

db = SQLAlchemy()
babel = Babel()