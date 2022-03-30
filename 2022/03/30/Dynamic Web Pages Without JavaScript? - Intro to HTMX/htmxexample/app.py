import requests
import os

from flask import Flask, render_template, request

app = Flask(__name__)

languages_frameworks = {
    'Python': ['Django', 'Flask', 'FastAPI'], 
    'Ruby': ['Rails', 'Sinatra'], 
    'JavaScript': ['Express', 'Hapi']}

api_key = os.environ.get('USDA_API_KEY')

@app.get('/dropdown')
def dropdown():
    return render_template('dropdown.html')

@app.get('/frameworks')
def frameworks():
    language = request.args.get('language')
    list_of_frameworks = languages_frameworks[language]
    return render_template('framework_options.html', list_of_frameworks=list_of_frameworks)

@app.get('/search')
def search():
    return render_template('search.html')

@app.get('/search_foods')
def search_foods():

    q = request.args.get('q')
    if q:
        r = requests.get(f'https://api.nal.usda.gov/fdc/v1/foods/search?query={q}&pageSize=50&api_key={api_key}')
        foods = r.json()['foods']

        return render_template('foods.html', foods=foods)
    return ''