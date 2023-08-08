from flask import Flask, request, render_template, Blueprint
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Song(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    performer = db.Column(db.String(100), nullable=False)
    chart_debut = db.Column(db.String(500), nullable=False)
    peak_position = db.Column(db.Integer, nullable=False)
    time_on_chart = db.Column(db.Integer, nullable=False)

main = Blueprint("main", __name__)

@main.route("/")
def index():
    return render_template("index.html")

@main.route("/search")
def search():
    q = request.args.get("q")
    print(q)

    if q:
        results = Song.query.filter(Song.title.icontains(q) | Song.performer.icontains(q)) \
        .order_by(Song.peak_position.asc()).order_by(Song.chart_debut.desc()).limit(100).all()
    else:
        results = []

    return render_template("search_results.html", results=results)

def create_app():
    app = Flask(__name__)
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///db.sqlite3"

    db.init_app(app)

    app.register_blueprint(main)

    return app