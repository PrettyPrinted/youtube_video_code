from django.db import models
import requests

class Location(models.Model):
    zip_code = models.IntegerField()
    latitude = models.DecimalField(blank=True, max_digits=9, decimal_places=6)
    longitude = models.DecimalField(blank=True, max_digits=9, decimal_places=6)


    def save(self, *args, **kwargs):
        r = requests.get(f'https://public.opendatasoft.com/api/records/1.0/search/?dataset=us-zip-code-latitude-and-longitude&q={self.zip_code}&facet=state&facet=timezone&facet=dst')
        self.latitude = r.json()['records'][0]['fields']['latitude']
        self.longitude = r.json()['records'][0]['fields']['longitude']
        super().save(*args, **kwargs)

    def __str__(self):
        return str(self.zip_code)