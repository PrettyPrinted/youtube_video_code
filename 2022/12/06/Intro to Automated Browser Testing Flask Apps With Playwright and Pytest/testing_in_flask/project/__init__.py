from flask import Flask

from .extensions import db, login_manager
from .models import User
from .routes import main


def create_app(database_uri="sqlite:///db.sqlite3"):
    app = Flask(__name__)
    app.config["SQLALCHEMY_DATABASE_URI"] = database_uri
    app.config["SECRET_KEY"] = "FesC9cBSuxakv9yN0vBY"

    db.init_app(app)
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(user_id)

    app.register_blueprint(main)
    return app
