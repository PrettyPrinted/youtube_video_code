from django.db import models

class Student(models.Model):
    name = models.CharField(max_length=20)
    major = models.ForeignKey('Subject', on_delete=models.CASCADE)
    minor = models.ForeignKey('Subject', related_name='minor_students', null=True, on_delete=models.CASCADE)

    def __str__(self):
        return self.name 

class Subject(models.Model):
    name = models.CharField(max_length=20)

    def __str__(self):
        return self.name