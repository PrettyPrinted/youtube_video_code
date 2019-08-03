from django.db import models

class Member(models.Model):
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    email = models.EmailField()
    city = models.CharField(max_length=30)
    ip_address = models.CharField(max_length=30)

    def __str__(self):
        return f'{ self.first_name } { self.last_name }'