from flask import Flask, session
from flask_sqlalchemy import SQLAlchemy 
from flask_session import Session 

app = Flask(__name__)

app.config['SECRET_KEY'] = 'mysecret'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite3'
app.config['SESSION_TYPE'] = 'sqlalchemy'

db = SQLAlchemy(app)

app.config['SESSION_SQLALCHEMY'] = db

sess = Session(app)

#db.create_all()

@app.route('/set/<value>')
def set_session(value):
    session['value'] = value 
    return f'The value you set is: { value }'

@app.route('/get')
def get_session():
    return f'The value in the session is: { session.get("value") }'