import click 
from flask.cli import with_appcontext

from .extensions import db
from .models import Customer, Order

@click.command(name='create_tables')
@with_appcontext
def create_tables():
    db.create_all()

@click.command(name='seed_data')
@with_appcontext
def seed_data():
    customer1 = Customer(
        name='John Doe', 
        address='123 Fake Street', 
        state='CA', 
        postal_code='90059'
    )

    db.session.add(customer1)

    customer2 = Customer(
        name='Curtis Brown', 
        address='456 Hollywood Blvd', 
        state='CA', 
        postal_code='90037'
    )

    db.session.add(customer2)

    customer3 = Customer(
        name='Priscilla Poole', 
        address='1111 Velvet Serene Ave.', 
        state='WA', 
        postal_code='48354'
    )

    db.session.add(customer3)

    customer4 = Customer(
        name='Eric Johnson', 
        address='555 Century Blvd.', 
        state='AZ', 
        postal_code='24068'
    )

    db.session.add(customer4)

    customer5 = Customer(
        name='Jane Smith', 
        address='789 Highway Rd', 
        state='CA', 
        postal_code='90015'
    )

    db.session.add(customer5)

    db.session.flush()

    order1 = Order(customer_id=customer1.id, total=29)
    order2 = Order(customer_id=customer1.id, total=99)
    order3 = Order(customer_id=customer1.id, total=145)
    order4 = Order(customer_id=customer1.id, total=300)
    order5 = Order(customer_id=customer1.id, total=12)
    order6 = Order(customer_id=customer1.id, total=25)
    order7 = Order(customer_id=customer1.id, total=78)
    order8 = Order(customer_id=customer1.id, total=102)
    order9 = Order(customer_id=customer1.id, total=2)

    db.session.add_all([order1, order2, order3, order4, order5, order6, order7, order8, order9])
    db.session.commit()

    order1 = Order(customer_id=customer2.id, total=29)
    order2 = Order(customer_id=customer2.id, total=99)
    order3 = Order(customer_id=customer2.id, total=145)
    order4 = Order(customer_id=customer2.id, total=300)
    order5 = Order(customer_id=customer2.id, total=12)
    order6 = Order(customer_id=customer2.id, total=25)
    order7 = Order(customer_id=customer2.id, total=78)
    order8 = Order(customer_id=customer2.id, total=102)
    order9 = Order(customer_id=customer2.id, total=2)

    db.session.add_all([order1, order2, order3, order4, order5, order6, order7, order8, order9])
    db.session.commit()

    order1 = Order(customer_id=customer3.id, total=29)
    order2 = Order(customer_id=customer3.id, total=99)
    order3 = Order(customer_id=customer3.id, total=145)
    order4 = Order(customer_id=customer3.id, total=300)
    order5 = Order(customer_id=customer3.id, total=12)
    order6 = Order(customer_id=customer3.id, total=25)
    order7 = Order(customer_id=customer3.id, total=78)
    order8 = Order(customer_id=customer3.id, total=102)
    order9 = Order(customer_id=customer3.id, total=2)

    db.session.add_all([order1, order2, order3, order4, order5, order6, order7, order8, order9])
    db.session.commit()

    order1 = Order(customer_id=customer4.id, total=29)
    order2 = Order(customer_id=customer4.id, total=99)
    order3 = Order(customer_id=customer4.id, total=145)
    order4 = Order(customer_id=customer4.id, total=300)
    order5 = Order(customer_id=customer4.id, total=12)
    order6 = Order(customer_id=customer4.id, total=25)
    order7 = Order(customer_id=customer4.id, total=78)
    order8 = Order(customer_id=customer4.id, total=102)
    order9 = Order(customer_id=customer4.id, total=2)

    db.session.add_all([order1, order2, order3, order4, order5, order6, order7, order8, order9])
    db.session.commit()

    order1 = Order(customer_id=customer5.id, total=29)
    order2 = Order(customer_id=customer5.id, total=99)
    order3 = Order(customer_id=customer5.id, total=145)
    order4 = Order(customer_id=customer5.id, total=300)
    order5 = Order(customer_id=customer5.id, total=12)
    order6 = Order(customer_id=customer5.id, total=25)
    order7 = Order(customer_id=customer5.id, total=78)
    order8 = Order(customer_id=customer5.id, total=102)
    order9 = Order(customer_id=customer5.id, total=2)

    db.session.add_all([order1, order2, order3, order4, order5, order6, order7, order8, order9])
    db.session.commit()
