from flask import Flask
from os import environ 

from .commands import create_users, create_database
from .extensions import db, guard
from .models import User 
from .routes import api 

def create_app():
    app = Flask(__name__)

    app.config['SECRET_KEY'] = environ.get('SECRET_KEY')
    app.config['SQLALCHEMY_DATABASE_URI'] = environ.get('SQLALCHEMY_DATABASE_URI')
    app.config['JWT_ACCESS_LIFESPAN'] = {'minutes' : 1}

    db.init_app(app)
    guard.init_app(app, User)

    app.cli.add_command(create_users)
    app.cli.add_command(create_database)

    app.register_blueprint(api)

    return app