from .models import Thread, Reply


def get_threads_service():
    return Thread.objects.all()

def create_threads_service(title, description):
    return Thread.objects.create(title=title, description=description)

def create_replies_service(thread_id, message, user):
    thread = Thread.objects.get(id=thread_id)
    reply = Reply.objects.create(thread=thread, message=message, user=user)
    return reply