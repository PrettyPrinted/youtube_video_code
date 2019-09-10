from django.shortcuts import render

from .tasks import send_email

def index(request):
    send_email.delay()
    #add(4,5)
    return render(request, 'index.html')
