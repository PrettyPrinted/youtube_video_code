from django.db import models

class Image(models.Model):
    url = models.URLField()
    prompt = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
