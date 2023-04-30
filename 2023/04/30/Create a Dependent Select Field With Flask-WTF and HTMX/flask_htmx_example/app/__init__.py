from flask import Flask

from .extensions import db
from .models import Country, City
from .routes import main 

def create_app():
    app = Flask(__name__)
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///db.sqlite3"
    app.config["SECRET_KEY"] = "thisisasecret!"
    
    db.init_app(app)
    app.register_blueprint(main)

    return app

def add_data():
    db.create_all()

    us = Country(name='United States')
    ca = Country(name='Canada')
    mx = Country(name='Mexico')

    db.session.add_all([us, ca, mx])

    db.session.add_all([
        City(name='New York City', country=us),
        City(name='Los Angeles', country=us),
        City(name='Chicago', country=us),
        City(name='Toronto', country=ca),
        City(name='Montreal', country=ca),
        City(name='Vancouver', country=ca),
        City(name='Mexico City', country=mx),
        City(name='Guadalajara', country=mx),
        City(name='Monterrey', country=mx)
    ])
    
    db.session.commit()