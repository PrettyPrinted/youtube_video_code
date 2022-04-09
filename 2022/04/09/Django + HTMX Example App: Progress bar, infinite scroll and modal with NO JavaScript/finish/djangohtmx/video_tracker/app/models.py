from django.db import models

class Channel(models.Model):
    name = models.CharField(max_length=200)
    playlist_id = models.CharField(max_length=200)
    thumbnail_url = models.CharField(max_length=200)
    description = models.TextField()


class Video(models.Model):
    title = models.CharField(max_length=200)
    views = models.IntegerField()
    likes = models.IntegerField()
    youtube_id = models.CharField(max_length=200)
    date_published = models.DateField()
    channel = models.ForeignKey(Channel, on_delete=models.CASCADE)