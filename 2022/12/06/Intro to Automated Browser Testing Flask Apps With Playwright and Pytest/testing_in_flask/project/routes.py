import requests

from flask import request, render_template, redirect, url_for, Blueprint
from flask_login import login_user, login_required, logout_user
from werkzeug.security import generate_password_hash, check_password_hash

from .extensions import db
from .models import Country, City, User

main = Blueprint("main", __name__)


@main.route("/")
def index():
    return render_template("index.html")


@main.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        email = request.form.get("email")
        password = request.form.get("password")

        user = User(email=email, password_hash=generate_password_hash(password))
        db.session.add(user)
        db.session.commit()

        return redirect(url_for("main.index"))

    return render_template("register.html")


@main.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form.get("email")
        password = request.form.get("password")

        user = User.query.filter_by(email=email).first()

        if user and check_password_hash(user.password_hash, password):
            login_user(user)
            return redirect(url_for("main.index"))

    return render_template("login.html")


@main.route("/logout")
@login_required
def logout_the_user():
    logout_user()
    return redirect(url_for("main.index"))


@main.route("/age", methods=["GET", "POST"])
@login_required
def get_age():
    age = None
    name = None

    if request.method == "POST":
        name = request.form.get("name")
        response = requests.get(f"https://api.agify.io/?name={name}").json()
        age = response["age"]
    return render_template("age.html", age=age, name=name)

@main.route("/city", methods=["GET", "POST"])
@login_required
def city_select():
    if request.method == "POST":
        city = request.form.get("city")
        country_id = request.form.get("country")
        db.session.add(City(name=city, country_id=country_id))
        db.session.commit()
        return redirect(url_for("main.city_select"))

    countries = Country.query.all()
    cities = City.query.all()
    return render_template("city.html", countries=countries, cities=cities)