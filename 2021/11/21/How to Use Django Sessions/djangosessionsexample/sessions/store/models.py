from django.db import models

class Product(models.Model):
    title = models.CharField(max_length=100)
    price = models.FloatField()
    description = models.TextField()
    image_url = models.CharField(max_length=100)
