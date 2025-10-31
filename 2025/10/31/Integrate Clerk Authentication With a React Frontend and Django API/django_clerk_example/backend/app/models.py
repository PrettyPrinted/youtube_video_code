from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    pass


class Channel(models.Model):
    name = models.CharField(max_length=255)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='channels')

    def __str__(self):
        return self.name


class Video(models.Model):
    title = models.CharField(max_length=255)
    channel = models.ForeignKey(Channel, on_delete=models.CASCADE, related_name='videos')

    def __str__(self):
        return self.title