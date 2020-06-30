from django.shortcuts import render

from .tasks import go_to_sleep

def index(request):
    task = go_to_sleep.delay(1)
    
    return render(request, 'example/index.html', {'task_id' : task.task_id})
