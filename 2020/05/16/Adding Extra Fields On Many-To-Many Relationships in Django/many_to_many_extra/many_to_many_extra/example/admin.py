from django.contrib import admin
from .models import Student, Course, Enrollment

admin.site.register(Student)
admin.site.register(Course)
admin.site.register(Enrollment)