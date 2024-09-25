from flask import Blueprint, render_template, request, redirect, url_for

from app.extensions import db
from app.models import Todo

main = Blueprint("main", __name__)

@main.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        db.session.add(Todo(task=request.form["task"]))
        db.session.commit()
        
        return redirect(url_for("main.index"))

    todos = Todo.query.all()

    return render_template("index.html", todos=todos)