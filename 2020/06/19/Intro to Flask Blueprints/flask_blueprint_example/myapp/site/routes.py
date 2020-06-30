from flask import Blueprint

site = Blueprint('site', __name__)

@site.route('/')
def index():
    return '<h1>Welcome to the home page!</h1>' 
