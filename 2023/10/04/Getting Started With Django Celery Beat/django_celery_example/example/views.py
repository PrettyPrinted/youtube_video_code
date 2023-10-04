from django.shortcuts import render
from django.http import HttpResponse

from django_celery_beat.models import PeriodicTask, IntervalSchedule

from .tasks import my_task

def index(request):
    my_task.delay()
    return HttpResponse("Task Started!")

def schedule_task(request):
    interval, _ = IntervalSchedule.objects.get_or_create(
        every=30,
        period=IntervalSchedule.SECONDS,
    )

    PeriodicTask.objects.create(
        interval=interval,
        name="my-schedule",
        task="example.tasks.my_task",
        #args=json.dumps(["Arg1", "Arg2"])
        #one_off=True
    )

    return HttpResponse("Task scheduled!")