from django.db import models

class Manager(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Amenity(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = 'Amenities'

class Property(models.Model):
    name = models.CharField(max_length=100)
    address = models.CharField(max_length=100)
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    zip_code = models.CharField(max_length=10)
    description = models.TextField()
    rent = models.IntegerField()
    availability = models.BooleanField(default=True)
    manager = models.ForeignKey(Manager, on_delete=models.CASCADE)
    amenities = models.ManyToManyField(Amenity)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = 'Properties'