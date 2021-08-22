from django.db import models

class Video(models.Model):
    youtube_id = models.CharField(max_length=20)
    title = models.CharField(max_length=200)
    description = models.TextField()

    def __str__(self):
        return self.title
