from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, SelectField, HiddenField, FormField, FieldList, Form
from wtforms.validators import DataRequired

class PhoneNumberForm(Form):
    id = HiddenField('id')
    phone_type = SelectField('Phone Type', choices=[("", "Select Type"), ('mobile', 'Mobile'), ('home', 'Home'), ('work', 'Work'), ('fax', 'Fax'), ('other', 'Other')], validators=[DataRequired()])
    country_code = IntegerField('Country Code', validators=[DataRequired()])
    area_code = IntegerField('Area Code', validators=[DataRequired()])
    number = StringField('Number', validators=[DataRequired()])

class PhoneNumbersForm(FlaskForm):
    phone_numbers = FieldList(FormField(PhoneNumberForm), min_entries=1)