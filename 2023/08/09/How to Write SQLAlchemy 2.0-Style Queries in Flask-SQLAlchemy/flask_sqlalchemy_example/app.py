from flask import Flask 
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite3'
db = SQLAlchemy(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))

#User.query.all()
#db.session.execute(db.select(User)).scalars().all()
#db.session.scalars(db.select(User)).all()

#User.query.first()
#db.session.scalars(db.select(User)).first()

#User.query.filter_by(name="Anthony").first()
#db.session.scalars(db.select(User).filter_by(name="Anthony")).first()

#User.query.filter(User.name != "Anthony").all()
#db.session.scalars(db.select(User).where(User.name != "Anthony")).all()

#User.query.get(4)
#db.session.get(User, 4)

#User.query.count()
#db.session.scalar(db.func.count(User.id))