from flask import Blueprint, render_template, redirect, url_for, request
from sqlalchemy import select

from .extensions import db
from .models import Images
from .tasks import generate_image

main = Blueprint('main', __name__)

@main.route('/', methods=["POST", "GET"])
def index():
    if request.method == "POST":
        generate_image.delay(request.form["prompt"])
        return redirect(url_for("main.index"))
    images = db.session.scalars(select(Images)).all()
    return render_template("index.html", images=images)
