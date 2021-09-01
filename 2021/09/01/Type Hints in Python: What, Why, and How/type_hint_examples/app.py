from flask import Flask 
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite3'
db = SQLAlchemy(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50))
    date_joined = db.Column(db.DateTime)

    @classmethod
    def create_user(cls, name: str) -> "User":
        return cls(name=name)


@app.route('/')
def index():
    user = User.create_user("Anthony")
    return "User created"