from flask import Flask
from flask_caching import Cache 

from random import randint 

from time import sleep

cache = Cache()

def create_app():
    app = Flask(__name__)

    app.config['CACHE_TYPE'] = 'simple'

    cache.init_app(app)

    @app.route('/')
    @cache.cached(timeout=5)
    def index():
        randnum = randint(1,1000)
        return f'<h1>The number is: {randnum}</h1>'

    @app.route('/number')
    def number():
        number = calculate()
        return f'<h1>The number is: {number}</h1>'

    @app.route('/sleep/<int:n>')
    def sleep_get(n):
        sleep_for(n)
        return '<h1>Done sleeping!</h1>'

    return app

@cache.cached(timeout=5, key_prefix='calculate')
def calculate():
    number = randint(5,100)
    return number

@cache.memoize(timeout=30)
def sleep_for(n):
    sleep(n)
    return 'Done!'