from django.contrib.auth.models import AbstractUser
from django.db import models

from django.conf import settings 

class User(AbstractUser):
    pass


# user = models.ForeignKey(settings.AUTH_USER_MODEL, )