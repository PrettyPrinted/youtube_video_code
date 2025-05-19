from flask import Blueprint, render_template

mod = Blueprint('site', __name__, template_folder='templates')

@mod.route('/homepage')
def homepage():
	return render_template('site/index.html')