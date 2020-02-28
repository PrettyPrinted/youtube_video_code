from django.db import models

class Member(models.Model):
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    email = models.EmailField()
    ip_address = models.GenericIPAddressField(protocol='IPv4')

