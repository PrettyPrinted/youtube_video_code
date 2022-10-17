from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask.ext.restless import APIManager

app = Flask(__name__)
app.config.from_pyfile('config.cfg')
db = SQLAlchemy(app)

class Person(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	name = db.Column(db.String(20))
	pets = db.relationship('Pet', backref='owner', lazy='dynamic')

class Pet(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	name = db.Column(db.String(20))
	owner_id = db.Column(db.Integer, db.ForeignKey('person.id'))

manager = APIManager(app, flask_sqlalchemy_db=db)

manager.create_api(Person)
manager.create_api(Pet)

if __name__ == "__main__":
	app.run(debug=True)