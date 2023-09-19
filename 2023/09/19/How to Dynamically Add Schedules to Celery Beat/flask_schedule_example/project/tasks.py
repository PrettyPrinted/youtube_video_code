from celery import shared_task
from time import sleep
from redbeat import RedBeatSchedulerEntry
from celery import current_app as celery_app

from .extensions import db
from .models import Result

@shared_task
def my_task(text, schedule_name):
    for i in range(10):
        sleep(1)
        print(i)
    result = Result(text=text)
    db.session.add(result)
    db.session.commit()

    try:
        entry = RedBeatSchedulerEntry.from_key("redbeat:"+schedule_name, app=celery_app)
    except KeyError:
        entry = None 

    if entry:
        entry.delete()