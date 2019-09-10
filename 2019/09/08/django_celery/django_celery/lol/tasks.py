from __future__ import absolute_import, unicode_literals
from celery import shared_task

from django.core.mail import send_mail

from time import sleep

@shared_task
def add(x, y):
    sleep(10)
    return x + y

@shared_task
def send_email():
    send_mail('Hello from PrettyPrinted',
    'Hello there. This is an automated message.',
    'support@prettyprinted.com',
    ['anthony@anthonyherbert.com'],
    fail_silently=False)

#celery -A django_celery worker -l info