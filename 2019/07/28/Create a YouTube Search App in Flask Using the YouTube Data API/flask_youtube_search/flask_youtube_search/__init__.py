from flask import Flask 

from .routes import main

def create_app(config_file='settings.py'):
    app = Flask(__name__)

    app.config.from_pyfile(config_file)

    app.register_blueprint(main)

    return app