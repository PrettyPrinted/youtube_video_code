from django.db import models

class Member(models.Model):
    name = models.CharField(max_length=20)
    region = models.CharField(max_length=2, choices=[('NA', 'North America'), ('EU', 'Europe')])
    moderator = models.BooleanField()

    def __str__(self):
        return self.name