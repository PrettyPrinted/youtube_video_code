from flask import Flask, render_template
from flask_wtf import FlaskForm
from wtforms import StringField
from wtforms.validators import ValidationError 

app = Flask(__name__)

app.config['SECRET_KEY'] = 'KR766ZRlzn3I4H8v.h2e:Jx!H;8NP('

class ApplicationForm(FlaskForm):
    name = StringField('name')

    def validate_name(self, field):
        if len(field.data) > 10:
            raise ValidationError('Field must be less than 10 characters')

def validate_length(self, field):
    if len(field.data) > 10:
        raise ValidationError('Field must be less than 10 characters')

@app.route('/', methods=['GET', 'POST'])
def index():
    #form = ApplicationForm()
    fields = {}
    with open('fields.txt') as f:
        for item in f.readlines():
            field_name = item.strip()
            fields[field_name] = StringField(field_name)
            fields['validate_'+field_name] = validate_length

    ApplicationFormDynamic = type('ApplicationFormDynamic', (FlaskForm, ), fields)
    form = ApplicationFormDynamic()

    if form.validate_on_submit():
        for field in form.data.keys():
            print(field, form.data[field])
    else:
        print(form.errors)

    return render_template('index.html', form=form)