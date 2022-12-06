from flask_login import UserMixin

from .extensions import db


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(100), unique=True)
    password_hash = db.Column(db.String(150))


class Country(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    cities = db.relationship('City', back_populates='country')

class City(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    country_id = db.Column(db.ForeignKey("country.id"))
    country = db.relationship('Country', back_populates='cities')
