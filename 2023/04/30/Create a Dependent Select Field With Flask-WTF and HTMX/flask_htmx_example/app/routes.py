from flask import Blueprint, render_template, request

from .forms import LocationForm
from .models import City

main = Blueprint('main', __name__)

@main.route('/', methods=["GET", "POST"])
def index():
    form = LocationForm()
    if form.country.data:
        form.city.query = City.query.filter_by(country_id=form.country.data.id).all()
    else:
        form.city.query = City.query.filter(None).all()

    if form.validate_on_submit():
        print(form.country.data.name)
        print(form.city.data.name)

    return render_template("index.html", form=form)

@main.route("/get_cities")
def get_cities():
    country_id = request.args.get("country", type=int)
    cities = City.query.filter_by(country_id=country_id).all()
    return render_template("city_options.html", cities=cities)