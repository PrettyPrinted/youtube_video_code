from flask import Flask, render_template, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from random import randint

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////mnt/c/Users/antho/Documents/ajax/database.db'

db = SQLAlchemy(app)

class Member(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50))
    email = db.Column(db.String(50))
    random = db.Column(db.Integer)

@app.route('/')
def index():
    members = Member.query.all()
    return render_template('index.html', members=members)
    
@app.route('/update', methods=['POST'])
def update():

    member = Member.query.filter_by(id=request.form['id']).first()
    member.name = request.form['name']
    member.email = request.form['email']
    member.random = randint(1,10000)

    db.session.commit()

    return jsonify({'result' : 'success', 'member_num' : member.random})

if __name__ == '__main__':
    app.run(debug=True)