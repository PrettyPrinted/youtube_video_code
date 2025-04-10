from django.db import models

class Coupon(models.Model):
    code = models.CharField(max_length=10, unique=True)
    discount = models.IntegerField()
    active = models.BooleanField()

    def __str__(self):
        return self.code


class Product(models.Model):
    name = models.CharField(max_length=100)
    price = models.IntegerField()
    description = models.TextField()

    def __str__(self):
        return self.name