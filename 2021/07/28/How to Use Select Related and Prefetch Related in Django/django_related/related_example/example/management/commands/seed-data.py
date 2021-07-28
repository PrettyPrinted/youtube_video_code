import random

from django.core.management.base import BaseCommand, CommandError
from faker import Faker 
from example.models import Customer, Product, Order, LineItem

fake = Faker()

def add_customers():
    for _ in range(100):
        customer = Customer(
            first_name=fake.first_name(),
            last_name=fake.last_name(),
            address=fake.street_address(),
            city=fake.city(),
            postcode=fake.postcode(),
            email=fake.email()
        )
        customer.save()

def add_orders():
    customers = Customer.objects.all()

    for _ in range(5000):
        #choose a random customer
        customer = random.choice(customers)

        ordered_date = fake.date_time_this_year()
        shipped_date = random.choices([None, fake.date_time_between(start_date=ordered_date)], [10, 90])[0]

        #choose either random None or random date for delivered and shipped
        delivered_date = None
        if shipped_date:
            delivered_date = random.choices([None, fake.date_time_between(start_date=shipped_date)], [50, 50])[0]

        #choose either random None or one of three coupon codes
        coupon_code = random.choices([None, '50OFF', 'FREESHIPPING', 'BUYONEGETONE'], [80, 10, 5, 5])[0]

        order = Order(
            customer_id=customer.id,
            order_date=ordered_date,
            shipped_date=shipped_date,
            delivered_date=delivered_date,
            coupon_code=coupon_code
        )

        order.save()

def add_products():
    for _ in range(10):
        product = Product(
            name=fake.catch_phrase(),
            price=random.randint(10,100)
        )
        product.save()
    
def add_order_products():
    orders = Order.objects.all()
    products = Product.objects.all()

    for order in orders:
        #select random k
        k = random.randint(1, 3)
        # select random products
        purchased_products = random.sample(list(products), k)
        #order.products.add(*purchased_products)
        for product in purchased_products:
            line_item = LineItem(order=order, product=product, quantity=random.randint(1, 5))
            line_item.save()

def create_random_data():
    add_customers()
    add_orders()
    add_products()
    add_order_products()

class Command(BaseCommand):
    def handle(self, *args, **options):
        create_random_data()