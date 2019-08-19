from flask import Flask

app = Flask(__name__)

@app.route('/')
def index():
    return {'somethingelse' : [1, 2, 3, 'a', 'd', 'f']}