from .extensions import db

class File(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    handle = db.Column(db.String(50))
    description = db.Column(db.String(50))
    filename = db.Column(db.String(50))