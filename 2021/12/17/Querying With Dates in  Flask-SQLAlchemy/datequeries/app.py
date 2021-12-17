from datetime import date, datetime, timedelta
from faker import Faker 
from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy 
from sqlalchemy import func

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite3'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

class Transactions(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    amount = db.Column(db.Integer)
    date_posted = db.Column(db.Date)
    datetime_posted = db.Column(db.DateTime)

@app.route('/')
def index():
    transactions = Transactions.query.all()

    #transaction_date = date(2020, 5, 25)
    #transactions = Transactions.query.filter_by(date_posted=transaction_date).all()

    #transaction_date = date(2021, 8, 25)
    #transactions = Transactions.query.filter(func.date(Transactions.datetime_posted) == transaction_date).all()

    #first_date = date(2019, 6, 13)
    #last_date = date(2019, 6, 16)
    #transactions = Transactions.query.filter(Transactions.date_posted.between(first_date, last_date)).all()

    #first_date = date(2019, 6, 13)
    #last_date = date(2019, 6, 16)
    #transactions = Transactions.query.filter(Transactions.datetime_posted.between(first_date, last_date)).all()

    #transactions = Transactions.query.filter(Transactions.date_posted > date.today() - timedelta(weeks=1)).all()

    #transactions = Transactions.query.filter(Transactions.datetime_posted > datetime.now() - timedelta(days=30)).all()

    #transactions = db.session.query(Transactions.date_posted, func.sum(Transactions.amount)).group_by(Transactions.date_posted).all()

    #transactions = db.session.query(func.strftime('%Y', Transactions.date_posted), func.sum(Transactions.amount)).group_by(func.strftime('%Y', Transactions.date_posted)).all()

    #transactions = db.session.query(func.strftime('%Y-%m', Transactions.date_posted), func.sum(Transactions.amount)).group_by(func.strftime('%Y-%m', Transactions.date_posted)).all()
    
    return render_template('index.html', transactions=transactions)

'''
db.create_all()

fake = Faker()

for _ in range(10000):
    transaction_date = fake.date_time_between(start_date='-3y')

    db.session.add(
        Transactions(
            amount=fake.random_int(),
            date_posted=transaction_date.date(),
            datetime_posted=transaction_date
        )
    )

db.session.commit()
'''