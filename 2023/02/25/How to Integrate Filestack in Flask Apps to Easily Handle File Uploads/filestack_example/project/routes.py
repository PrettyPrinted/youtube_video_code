import json

from flask import Blueprint, render_template, request, url_for, redirect

from .models import File 
from .extensions import db

main = Blueprint("main", __name__)

@main.route("/", methods=["POST", "GET"])
def index():
    if request.method == "POST":
        for item in request.form.getlist("file-upload"):
            file_data = json.loads(item)
            description = request.form["description"]

            f = File(handle=file_data["handle"], filename=file_data["filename"], description=description)
            db.session.add(f)
        db.session.commit()

        return redirect(url_for("main.index"))

    files = File.query.all()
    return render_template("index.html", files=files)