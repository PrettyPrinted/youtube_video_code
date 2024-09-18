from .extensions import db

class Reservation(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    date = db.Column(db.Date, nullable=False)
    guests = db.Column(db.Integer, nullable=False)
    nights = db.Column(db.Integer, nullable=False)
    room = db.Column(db.String(10), nullable=False)
    amount = db.Column(db.Integer, nullable=False)
    currency = db.Column(db.String(4), nullable=False)