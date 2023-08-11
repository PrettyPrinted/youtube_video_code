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


# You can run this function in the flask shell after creating the database
def load_data():
    # You can download the CSV from the following link.
    # https://github.com/HipsterVizNinja/random-data/tree/main/Music/hot-100
    song_data = {}
    with open("data.csv") as f:
        reader = csv.DictReader(f)
        for row in reader:
            if (row["song"], row["performer"]) not in song_data:
                song_data[(row["song"], row["performer"])] = {
                    "chart_debut": row["chart_debut"],
                    "peak_position": int(row["peak_position"]),
                    "time_on_chart": int(row["time_on_chart"])
                }
            else:
                song_data[(row["song"], row["performer"])]["peak_position"] = min(song_data[(row["song"], row["performer"])]["peak_position"], int(row["peak_position"]))
                song_data[(row["song"], row["performer"])]["time_on_chart"] = max(song_data[(row["song"], row["performer"])]["time_on_chart"], int(row["time_on_chart"]))

    for s in song_data:
        song = Song(title=s[0], performer=s[1], chart_debut=song_data[s]["chart_debut"], peak_position=song_data[s]["peak_position"], time_on_chart=song_data[s]["time_on_chart"])
        db.session.add(song)


    db.session.commit() 

