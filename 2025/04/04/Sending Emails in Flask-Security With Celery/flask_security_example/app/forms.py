from flask_security import RegisterFormV2
from wtforms import StringField, validators

class ExtendedRegisterForm(RegisterFormV2):
    name = StringField("name", validators=[validators.DataRequired()])