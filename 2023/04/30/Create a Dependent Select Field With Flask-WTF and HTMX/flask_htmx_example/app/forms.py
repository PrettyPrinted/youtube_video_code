from flask_wtf import FlaskForm
from wtforms_sqlalchemy.fields import QuerySelectField

from .models import Country

class LocationForm(FlaskForm):
    country = QuerySelectField('Country', query_factory=lambda: Country.query.all(), allow_blank=True, get_label="name")
    city = QuerySelectField('City', get_label="name", allow_blank=True)