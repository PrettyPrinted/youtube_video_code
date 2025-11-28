from django.shortcuts import render

from .models import Item

def index(request):
    items = Item.objects.all().prefetch_related('details')
    return render(request, 'index.html', {'items': items})
