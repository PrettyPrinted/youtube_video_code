from django.db import models

class Member(models.Model):
    name = models.CharField(max_length=20)
    membership_number = models.CharField(max_length=10)