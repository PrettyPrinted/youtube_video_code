from flask import Blueprint, jsonify, request
from . import db 
from .models import Movie

main = Blueprint('main', __name__)

@main.route('/add_movie', methods=['POST'])
def add_movie():
    movie_data = request.get_json()

    new_movie = Movie(title=movie_data['title'], rating=movie_data['rating'])

    db.session.add(new_movie)
    db.session.commit()

    return 'Done', 201

@main.route('/movies')
def movies():
    movie_list = Movie.query.all()
    movies = []

    for movie in movie_list:
        movies.append({'title' : movie.title, 'rating' : movie.rating})

    return jsonify({'movies' : movies})