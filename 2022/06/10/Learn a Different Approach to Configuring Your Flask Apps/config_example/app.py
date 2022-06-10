from flask import Flask 

import os

def create_app():
    app = Flask(__name__)

    app.config.from_prefixed_env()
    #print(app.config['SECRET_KEY'])
    print(app.config['SQLALCHEMY_DATABASE_URI'])

    return app