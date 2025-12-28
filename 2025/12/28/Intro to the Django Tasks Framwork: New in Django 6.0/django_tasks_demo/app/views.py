from django.http import HttpResponse

from .tasks import example_task

def index(request):
    example_task.enqueue()
    return HttpResponse("Started task.")
