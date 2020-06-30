from flask import Blueprint, render_template

site = Blueprint('site', __name__, template_folder='templates')

@site.route('/')
def index():
    return render_template('site/index.html')