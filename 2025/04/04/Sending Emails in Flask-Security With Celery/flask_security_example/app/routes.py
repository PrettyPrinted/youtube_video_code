from flask import Blueprint, render_template
from flask_security import auth_required, roles_accepted

main = Blueprint("main", __name__)

@main.route("/")
@auth_required()
def index():
    return render_template("index.html")

@main.route("/admin")
@roles_accepted("admin")
def admin():
    return "<h1>Admin</h1>"