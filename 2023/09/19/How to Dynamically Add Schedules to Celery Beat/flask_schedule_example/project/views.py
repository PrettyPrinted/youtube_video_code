from flask import Blueprint
from redbeat import RedBeatSchedulerEntry
from redbeat.schedules import rrule
from datetime import datetime 
from celery import current_app as celery_app

from uuid import uuid4

from .tasks import my_task

main = Blueprint("main", __name__)

@main.route("/", methods=["GET"])
def index():
    #my_task.delay("Hello World!")
    schedule_name = str(uuid4())
    dt = datetime.utcnow()
    interval = rrule(freq="MINUTELY", dtstart=dt)                              
    entry = RedBeatSchedulerEntry(schedule_name, 
        "project.tasks.my_task", 
        interval, 
        args=["From the scheduler"], 
        kwargs={"schedule_name": schedule_name},
        app=celery_app
    )
    entry.save()
    return "Created the schedule!"