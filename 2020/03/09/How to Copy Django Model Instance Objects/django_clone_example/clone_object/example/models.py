from django.db import models

class Member(models.Model):
    name = models.CharField(max_length=50)
    location = models.CharField(max_length=50)
