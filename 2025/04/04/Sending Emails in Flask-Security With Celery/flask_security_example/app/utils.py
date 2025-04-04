from celery import shared_task
from flask_security import MailUtil
from flask_mailman import EmailMultiAlternatives
from .extensions import mail

@shared_task
def send_flask_mail(**kwargs):
    with mail.get_connection() as connection:
        html = kwargs.pop("html", None)
        msg = EmailMultiAlternatives(
            **kwargs,
            connection=connection,
        )
        if html:
            msg.attach_alternative(html, "text/html")
        msg.send()

class CeleryMailUtil(MailUtil):
    def send_mail(self, template, subject, recipient, sender, body, html, **kwargs):
        send_flask_mail.delay(subject=subject, body=body, html=html, from_email=sender, to=[recipient])