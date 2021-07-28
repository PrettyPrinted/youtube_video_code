from django.shortcuts import render

from .models import Order

def index(request):
    #orders = Order.objects.select_related('customer').all()
    orders = Order.objects.prefetch_related('products').all()

    for order in orders:
        for product in order.products.all():
            temp = product
    return render(request, 'index.html')
