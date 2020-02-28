import csv

from django.shortcuts import render
from django.http import HttpResponse

from .models import Member

def export(request):
    response = HttpResponse(content_type='text/csv')

    writer = csv.writer(response)
    writer.writerow(['First Name', 'Last Name', 'Email', 'IP Address'])

    for member in Member.objects.all().values_list('first_name', 'last_name', 'email', 'ip_address'):
        writer.writerow(member)

    response['Content-Disposition'] = 'attachment; filename="members.csv"'

    return response
