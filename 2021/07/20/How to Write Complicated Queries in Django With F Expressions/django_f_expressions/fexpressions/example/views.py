from django.http import HttpResponse
from django.db.models import F, Sum, Avg
from datetime import timedelta

from .models import Customer, Product, Order, LineItem

def index(request):
    '''
    line_items = LineItem.objects.annotate(sub_total=F('product__price') * F('quantity'))

    for line_item in line_items:
        print(line_item.quantity, line_item.product.price, line_item.sub_total)
    '''

    '''
    result = LineItem.objects.aggregate(total=Avg(F('product__price') * F('quantity')))
    print(result['total'])
    '''

    '''
    orders = Order.objects.filter(order_date=F('shipped_date'))
    for order in orders:
        print(order.order_date, order.shipped_date)
    '''

    orders = Order.objects.annotate(processing_time=F('shipped_date') - F('order_date')).filter(processing_time__lt=timedelta(days=3))
    for order in orders:
        print(order.order_date, order.shipped_date)
        
    return HttpResponse(f'')