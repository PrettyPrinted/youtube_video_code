import threading

from flask import Blueprint, render_template, request, redirect, url_for, current_app
from uuid import uuid4
from sqlalchemy import select

from .extensions import db
from .models import File
from .tasks import process_file

main = Blueprint("main", __name__)

@main.route("/")
def index():
    stmt = select(File)
    files = db.session.scalars(stmt)
    return render_template("index.html", files=files)

@main.route("/file/<int:id>")
def file(id):
    stmt = select(File).where(File.id == id)
    file = db.session.execute(stmt).scalar_one()
    return render_template("file.html", file=file)

@main.route("/upload", methods=["POST"])
def upload():
    f = request.files["file"]
    extension = f.filename.split(".")[-1]
    path = f"files/{uuid4()}.{extension}"
    f.save(path)
    threading.Thread(target=process_file, args=(current_app.app_context(), f.filename, path)).start()
    return redirect(url_for("main.index"))