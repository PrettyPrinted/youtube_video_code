from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy 
from flask_wtf import FlaskForm 
from wtforms_sqlalchemy.fields import QuerySelectField

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////mnt/c/Users/antho/Documents/queryselectexample/test.db'
app.config['SECRET_KEY'] = 'secret'

db = SQLAlchemy(app)

class Choice(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50))
    extra = db.Column(db.String(50))

    def __repr__(self):
        return '[Choice {}]'.format(self.name)

def choice_query():
    return Choice.query

class ChoiceForm(FlaskForm):
    opts = QuerySelectField(query_factory=choice_query, allow_blank=False, get_label='name')

@app.route('/', methods=['GET', 'POST'])
def index():
    form = ChoiceForm()

    form.opts.query = Choice.query.filter(Choice.id > 1)

    if form.validate_on_submit():
        return '<html><h1>{}</h1></html>'.format(form.opts.data)

    return render_template('index.html', form=form)

if __name__ == '__main__':
    app.run(debug=True)