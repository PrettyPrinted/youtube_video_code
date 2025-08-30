from flask import Flask 
from flask_sqlalchemy_lite import SQLAlchemy 
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship
from sqlalchemy import String, ForeignKey, Table, Column, select, func
from typing import Optional, List
from datetime import datetime, timezone, timedelta
from faker import Faker
import random

app = Flask(__name__)
app.config["SQLALCHEMY_ENGINES"] = {"default": "sqlite:///db.sqlite3"}

db = SQLAlchemy()
db.init_app(app)

class Base(DeclarativeBase):
    pass


class Customer(Base):
    __tablename__ = "customer"

    id: Mapped[int] = mapped_column(primary_key=True)
    first_name: Mapped[str] = mapped_column(String(50))
    last_name: Mapped[str] = mapped_column(String(50))
    address: Mapped[str] = mapped_column(String(500))
    city: Mapped[str] = mapped_column(String(50))
    postcode: Mapped[str] = mapped_column(String(50))
    email: Mapped[str] = mapped_column(String(50), unique=True)

    customer_order: Mapped[List["CustomerOrder"]] = relationship(back_populates="customer")

    def __repr__(self):
        return f"{self.first_name} {self.last_name}"

customer_order_product = Table(
    "customer_order_product",
    Base.metadata,
    Column("customer_order_id", ForeignKey("customer_order.id"), primary_key=True),
    Column("product_id", ForeignKey("product.id"), primary_key=True)
)

class CustomerOrder(Base):
    __tablename__ = "customer_order"

    id: Mapped[int] = mapped_column(primary_key=True)
    customer_id: Mapped[int] = mapped_column(ForeignKey("customer.id"))
    order_date: Mapped[datetime] = mapped_column(default=datetime.now(timezone.utc))
    shipped_date: Mapped[Optional[datetime]]
    delivered_date: Mapped[Optional[datetime]]
    coupon_code: Mapped[Optional[str]] = mapped_column(String(10))

    customer: Mapped[List["Customer"]] = relationship(back_populates="customer_order")
    products: Mapped[List["Product"]] = relationship(secondary="customer_order_product", back_populates="customer_orders")

class Product(Base):
    __tablename__ = "product"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(50), unique=True)
    price: Mapped[int]

    customer_orders: Mapped[List["CustomerOrder"]] = relationship(secondary="customer_order_product", back_populates="products")

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
        db.session.add(customer)
    db.session.commit()

def add_orders():
    customers = db.session.scalars(select(Customer)).all()

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

        order = CustomerOrder(
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
    orders = db.session.scalars(select(CustomerOrder)).all()
    products = db.session.scalars(select(Product)).all()

    for order in orders:
        #select random k
        k = random.randint(1, 3)
        # select random products
        purchased_products = random.sample(products, k)
        order.products.extend(purchased_products)
        
    db.session.commit()

def create_random_data():
    Base.metadata.create_all(db.engine)
    add_customers()
    add_orders()
    add_products()
    add_order_products()


def get_orders_by(customer_id=1):
    print("Get Orders by Customer")
    stmt = select(CustomerOrder).where(CustomerOrder.customer_id == customer_id)
    customer_orders = db.session.scalars(stmt).all()
    for order in customer_orders:
        print(
            order.customer.first_name,
            order.id,
            order.order_date,
            order.shipped_date,
            order.delivered_date,
            order.coupon_code
        )

def get_pending_orders():
    print("Pending Orders")
    stmt = select(CustomerOrder).where(CustomerOrder.shipped_date.is_(None))
    pending_orders = db.session.scalars(stmt).all()
    for order in pending_orders:
        print(order.id, order.order_date)

def how_many_customers():
    print("How many customers?")
    stmt = select(func.count()).select_from(Customer)
    count = db.session.scalar(stmt)
    print(count)

def revenue_in_last_x_days(x_days=30):
    print("revenue in last x days")
    stmt  = select(func.sum(Product.price)).select_from(Product)\
        .join(customer_order_product)\
        .join(CustomerOrder)\
        .where(CustomerOrder.order_date > (datetime.now() - timedelta(days=x_days)))
    revenue = db.session.scalar(stmt)
    print(revenue)