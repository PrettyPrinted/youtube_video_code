from flask import Blueprint

from .extensions import mongo 

main = Blueprint('main', __name__)

@main.route('/')
def index():
    user_collection = mongo.db.users
    user_collection.insert({'name' : 'Emily', 'language' : 'Python'})
    user_collection.insert({'name' : 'Frank', 'language' : 'C'})
    return '<h1>Added a User!</h1>'

@main.route('/find')
def find():
    user_collection = mongo.db.users 
    user = user_collection.find_one({'name' : 'Emily'})
    return f'<h1>User: { user["name"] } Language: { user["language"] }</h1>'

@main.route('/update')
def update():
    user_collection = mongo.db.users 
    user = user_collection.find_one({'name' : 'Emily'})
    user["language"] = 'Ruby'

    user_collection.save(user)

    return '<h1>Updated user!</h1>'

@main.route('/delete')
def delete():
    user_collection = mongo.db.users 
    user = user_collection.find_one({'name' : 'Brian'})

    user_collection.remove(user)

    return '<h1>Deleted User!</h1>'