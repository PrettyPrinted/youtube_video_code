from django.db import models

class Framework(models.Model):
    name = models.CharField(max_length=255)
    language = models.CharField(max_length=255)
