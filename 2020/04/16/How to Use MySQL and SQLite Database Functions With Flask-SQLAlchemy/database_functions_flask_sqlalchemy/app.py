from flask import Flask 
from flask_sqlalchemy import SQLAlchemy 

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite3'
#app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://VW4XVmDgKU:MBxl2ElQqs@remotemysql.com:3306/VW4XVmDgKU'

db = SQLAlchemy(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(100))
    last_name = db.Column(db.String(100))
    email = db.Column(db.String(100))
    ip_address = db.Column(db.String(100))
    country = db.Column(db.String(100))
    date_joined = db.Column(db.Date)


#db.session.query(db.func.avg(User.id)).scalar()
#db.session.query(db.func.sum(User.id)).scalar()
#db.session.query(db.func.min(User.id)).scalar()
#db.session.query(db.func.max(User.id)).scalar()
#db.session.query(db.func.dayname(User.date_joined)).all()
#db.session.query(User.email, db.func.dayname(User.date_joined)).filter(db.func.dayname(User.date_joined) == 'Monday').all()