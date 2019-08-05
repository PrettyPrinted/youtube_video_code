from flask import Blueprint, jsonify, request
from flask_praetorian import auth_required
from .extensions import guard

api = Blueprint('api', __name__)

@api.route('/login', methods=['POST'])
def login():
    json_data = request.get_json()
    username = json_data['username']
    password = json_data['password']

    user = guard.authenticate(username, password)
    token = guard.encode_jwt_token(user)
    print(token)
    return jsonify({'access_token' : token})

@api.route('/protected')
@auth_required
def protected():
    return jsonify({'result' : 'You are in a special area!'}) 

@api.route('/refresh')
def refresh():
    json_data = request.get_json()
    token = guard.refresh_jwt_token(json_data['token'])
    return jsonify({'access_token' : token})

@api.route('/open')
def open():
    return jsonify({'result' : 'Hello'})