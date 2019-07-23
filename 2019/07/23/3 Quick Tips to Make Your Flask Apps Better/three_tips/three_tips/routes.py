from flask import Blueprint, render_template

from .extensions import db
from .models import Customer, Order

main = Blueprint('main', __name__)

@main.route('/<int:customer_id>')
def index(customer_id):
    customer = Customer.query.get_or_404(customer_id)

    context = {
        'name' : customer.name,
        'address' : customer.address,
        'state' : customer.state,
        'postal_code' : customer.postal_code
    }

    return render_template('index.html', **context)

@main.route('/delete')
def delete():
    order_ids = db.session.query(Order.id).join(Customer).filter(Customer.state == 'CA')

    delete_count = db.session.query(Order).filter(Order.id.in_(order_ids.subquery())).delete(
        synchronize_session=False)

    return str(delete_count)