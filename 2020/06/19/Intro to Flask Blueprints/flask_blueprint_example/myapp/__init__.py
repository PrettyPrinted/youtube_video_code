from flask import Flask 

from .api.routes import api 
from .site.routes import site

def create_app():
    app = Flask(__name__)

    app.register_blueprint(api)
    app.register_blueprint(site)

    return app
