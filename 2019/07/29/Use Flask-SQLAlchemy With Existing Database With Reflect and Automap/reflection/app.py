from flask import Flask 
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.ext.automap import automap_base

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite3'

db = SQLAlchemy(app)

# customer = db.Table('customer', db.metadata, autoload=True, autoload_with=db.engine)

Base = automap_base()
Base.prepare(db.engine, reflect=True)
Product = Base.classes.product
Order = Base.classes.order

@app.route('/')
def index():
    #new_product = Product(name='New Product', price=50, monthly_goal=1000)
    #db.session.add(new_product)
    #db.session.commit()

    #results = db.session.query(Product).all()
    #for r in results:
    #    print(r.name)

    order_count = db.session.query(Order).join(Product).filter(Product.id == 2).count()
    print(order_count)

    return ''