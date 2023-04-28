from flask import Flask, make_response, request

from .utils import auth_required

def create_app():
    app = Flask(__name__)

    app.config.from_prefixed_env()

    @app.route("/")
    @auth_required
    def index():
        return "<h1>Hello, World!</h1>"

    @app.route("/home")
    @auth_required
    def home():
        return "<h1>Home!</h1>"

    return app