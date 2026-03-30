from django.db import models

from django.db import models
from django.urls import reverse

class Event(models.Model):
    name = models.CharField(max_length=200)
    event_date = models.DateField()

    def get_absolute_url(self):
        return reverse("detail_view_example", kwargs={"pk": self.pk})
