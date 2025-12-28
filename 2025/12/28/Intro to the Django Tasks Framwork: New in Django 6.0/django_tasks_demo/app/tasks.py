from django.tasks import task

@task
def example_task():
    print("Task is running...")