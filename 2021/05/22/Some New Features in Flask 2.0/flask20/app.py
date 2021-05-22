from flask import Flask, Blueprint, abort

import asyncio 

app = Flask(__name__)

@app.route('/', methods=['GET'])
def index():
    abort(400)
    return "Hello, World!"

api = Blueprint('api', __name__, url_prefix='/api')
members_api = Blueprint('members_api', __name__, url_prefix='/members')

@api.errorhandler(400)
def api_bad_request(e):
    return {'status': 'bad request'}

@members_api.get('/')
def members_index():
    abort(400)
    return {}

api.register_blueprint(members_api)
app.register_blueprint(api)

@app.get('/async')
async def async_demo():
    await asyncio.sleep(3)
    return '<h1>Async Done</h1>'