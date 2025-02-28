import markdown2

from flask import Flask 

from .extensions import db
from .routes import main

def create_app():
    app = Flask(__name__)
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///db.sqlite3"

    db.init_app(app)

    app.register_blueprint(main)
    
    @app.template_filter("to_markdown")
    def to_markdown(text):
        return markdown2.markdown(text)

    return app