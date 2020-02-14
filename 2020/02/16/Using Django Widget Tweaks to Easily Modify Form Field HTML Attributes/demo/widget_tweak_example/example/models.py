from django.db import models

class Contact(models.Model):
    PURPOSE_CHOICES = [
        ('IN', 'Inquiry'),
        ('CO', 'Complaint'),
        ('FB', 'Feedback'),
    ]

    name = models.CharField(max_length=100)
    email = models.EmailField(max_length=100)
    purpose = models.CharField(max_length=2, choices=PURPOSE_CHOICES)
    message = models.TextField()
