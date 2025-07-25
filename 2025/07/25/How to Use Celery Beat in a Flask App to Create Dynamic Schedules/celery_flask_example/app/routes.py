from flask import Blueprint, render_template, redirect, url_for, request
from sqlalchemy import select
from redbeat import RedBeatSchedulerEntry
from celery import current_app as celery_app
from uuid import uuid4
from celery.schedules import schedule

from .extensions import db
from .models import Images
from .tasks import generate_image

main = Blueprint('main', __name__)

@main.route('/', methods=["POST", "GET"])
def index():
    if request.method == "POST":
        # generate_image.delay(request.form["prompt"])
        schedule_name = str(uuid4())
        interval = schedule(int(request.form["interval"]))
        entry = RedBeatSchedulerEntry(
            schedule_name,
            "app.tasks.generate_image",
            interval,
            args=[request.form["prompt"], schedule_name],
            app=celery_app
        )
        entry.save()
        return redirect(url_for("main.index"))
    images = db.session.scalars(select(Images)).all()
    return render_template("index.html", images=images)
