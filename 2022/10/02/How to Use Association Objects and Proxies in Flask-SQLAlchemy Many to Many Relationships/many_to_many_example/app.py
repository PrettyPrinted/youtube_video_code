from flask import Flask
from flask_sqlalchemy import SQLAlchemy 
from sqlalchemy.ext.associationproxy import association_proxy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite3'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

#user_channel = db.Table('user_channel',
#    db.Column('user_id', db.Integer, db.ForeignKey('user.id')),
#    db.Column('channel_id', db.Integer, db.ForeignKey('channel.id'))
#)

class UserChannel(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column('user_id', db.Integer, db.ForeignKey('user.id'))
    channel_id = db.Column('channel_id', db.Integer, db.ForeignKey('channel.id'))
    date_followed = db.Column(db.DateTime)

    user = db.relationship('User', back_populates='channel_association')
    channel = db.relationship('Channel', back_populates='users')

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20))
    channel_association = db.relationship('UserChannel', back_populates='user')
    channels = association_proxy("channel_association", "channel")

    def __repr__(self):
        return f'<User: {self.name}>'

class Channel(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20))
    users = db.relationship('UserChannel', back_populates='channel')

    def __repr__(self):
        return f'<Channel: {self.name}>'