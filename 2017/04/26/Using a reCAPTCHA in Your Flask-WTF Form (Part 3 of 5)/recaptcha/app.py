from flask import Flask, render_template
from flask_wtf import FlaskForm, RecaptchaField
from wtforms import StringField, PasswordField
from wtforms.validators import InputRequired, Length, AnyOf

app = Flask(__name__)
app.config['SECRET_KEY'] = 'Thisisasecret!'
app.config['RECAPTCHA_PUBLIC_KEY'] = 'YOUR-PUBLIC-KEY'
app.config['RECAPTCHA_PRIVATE_KEY'] = 'YOUR-SECRET-KEY'
app.config['TESTING'] = True

class LoginForm(FlaskForm):
    username = StringField('username', validators=[InputRequired('A username is required!'), Length(min=5, max=10, message='Must be between 5 and 10 characters.')])
    password = PasswordField('password', validators=[InputRequired('Password is required!'), AnyOf(values=['password', 'secret'])])
    recaptcha = RecaptchaField()

@app.route('/form', methods=['GET', 'POST'])
def form():
    form = LoginForm()

    if form.validate_on_submit():
        return '<h1>The username is {}. The password is {}.'.format(form.username.data, form.password.data)
    return render_template('form.html', form=form)

if __name__ == '__main__':
    app.run(debug=True)