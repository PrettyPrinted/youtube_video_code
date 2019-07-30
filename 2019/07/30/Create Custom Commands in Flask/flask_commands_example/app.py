from flask import Flask 
import click
from flask.cli import with_appcontext
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite3'

db = SQLAlchemy(app)

class MyTable(db.Model):
    id = db.Column(db.Integer, primary_key=True)

@click.command(name='create')
@with_appcontext
def create():
    db.create_all()

app.cli.add_command(create)