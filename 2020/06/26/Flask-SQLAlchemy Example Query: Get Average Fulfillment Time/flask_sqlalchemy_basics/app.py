from flask import Flask 
from flask_sqlalchemy import SQLAlchemy

from datetime import datetime, timedelta
from faker import Faker 

import random

fake = Faker()

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite3'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False 
db = SQLAlchemy(app)
#db.init_app(app)

class Customer(db.Model):
    id = db.Column(db.Integer, primary_key=True) 
    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)
    address = db.Column(db.String(500), nullable=False)
    city = db.Column(db.String(50), nullable=False)
    postcode = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(50), nullable=False, unique=True)

    orders = db.relationship('Order', backref='customer')

order_product = db.Table('order_product',
    db.Column('order_id', db.Integer, db.ForeignKey('order.id'), primary_key=True),
    db.Column('product_id', db.Integer, db.ForeignKey('product.id'), primary_key=True)
)

class Order(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    order_date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    shipped_date = db.Column(db.DateTime)
    delivered_date = db.Column(db.DateTime)
    coupon_code = db.Column(db.String(50))
    customer_id = db.Column(db.Integer, db.ForeignKey('customer.id'), nullable=False)

    products = db.relationship('Product', secondary=order_product)

class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False, unique=True)
    price = db.Column(db.Integer, nullable=False)

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
        db.session.add(customer)
    db.session.commit()

def add_orders():
    customers = Customer.query.all()

    for _ in range(1000):
        #choose a random customer
        customer = random.choice(customers)

        ordered_date = fake.date_time_this_year()
        shipped_date = random.choices([None, fake.date_time_between(start_date=ordered_date)], [10, 90])[0]

        #choose either random None or random date for delivered and shipped
        delivered_date = None
        if shipped_date:
            delivered_date = random.choices([None, fake.date_time_between(start_date=shipped_date)], [50, 50])[0]

        #choose either random None or one of three coupon codes
        coupon_code = random.choices([None, '50OFF', 'FREESHIPPING', 'BUYONEGETONE'], [80, 5, 5, 5])[0]

        order = Order(
            customer_id=customer.id,
            order_date=ordered_date,
            shipped_date=shipped_date,
            delivered_date=delivered_date,
            coupon_code=coupon_code
        )

        db.session.add(order)
    db.session.commit()

def add_products():
    for _ in range(10):
        product = Product(
            name=fake.color_name(),
            price=random.randint(10,100)
        )
        db.session.add(product)
    db.session.commit()
    
def add_order_products():
    orders = Order.query.all()
    products = Product.query.all()

    for order in orders:
        #select random k
        k = random.randint(1, 3)
        # select random products
        purchased_products = random.sample(products, k)
        order.products.extend(purchased_products)
        
    db.session.commit()

def create_random_data():
    db.create_all()
    add_customers()
    add_orders()
    add_products()
    add_order_products()

def get_orders_by(customer_id=1):
    print('Get Orders by Customer')
    customer_orders = Order.query.filter_by(customer_id=customer_id).all()
    for order in customer_orders:
        print(order.order_date)

def get_pending_orders():
    print('Pending Orders')
    pending_orders = Order.query.filter(Order.shipped_date.is_(None)).order_by(Order.order_date.desc()).all()
    for order in pending_orders:
        print(order.order_date)

def how_many_customers():
    print('How many customers?')
    print(Customer.query.count())

def orders_with_code():
    print('Orders with coupon code')
    orders = Order.query.filter(Order.coupon_code.isnot(None)).filter(Order.coupon_code != 'FREESHIPPING').all()
    for order in orders:
        print(order.coupon_code)

def revenue_in_last_x_days(x_days=30):
    print('Revenue past x days')
    print(db.session
        .query(db.func.sum(Product.price))
        .join(order_product).join(Order)
        .filter(Order.order_date > (datetime.now() - timedelta(days=x_days))
        ).scalar()
    )

def average_fulfillment_time():
    print('Average fulfillment time')
    print(
        db.session.query(
            db.func.time(
                db.func.avg(
                    db.func.strftime('%s', Order.shipped_date) - db.func.strftime('%s', Order.order_date)
                ), 
                'unixepoch'
            )
        ).filter(Order.shipped_date.isnot(None)).scalar()
    )

def get_customers_who_have_purchased_x_dollars(amount=500):
    print('All customers who have purchased x dollars')
    customers = db.session.query(Customer).join(Order).join(order_product).join(Product).group_by(Customer).having(db.func.sum(Product.price) > amount).all()
    for customer in customers:
        print(customer.first_name)