from flask import Flask 
from flask_sqlalchemy import SQLAlchemy 
from flask_admin import Admin 
from flask_admin.contrib.sqla import ModelView

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////mnt/c/Users/antho/Documents/workout.db'
app.config['SECRET_KEY'] = 'mysecret'
db = SQLAlchemy(app)
admin = Admin(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20))
    password = db.Column(db.Unicode(100))
    units = db.Column(db.String(3))
    workouts = db.relationship('Workout', backref='user', lazy='dynamic')

    def __repr__(self):
        return '<User %r>' % (self.name)

class Workout(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.DateTime)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    notes = db.Column(db.Text)
    bodyweight = db.Column(db.Numeric)
    exercises = db.relationship('Exercise', backref='workout', lazy='dynamic')

    def __repr__(self):
        return '<Workout %r>' % (self.id)

class Exercises(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50))
    exercise = db.relationship('Exercise', backref='exercise', lazy='dynamic')

    def __repr__(self):
        return '<Exercises %r>' % (self.name)

class Exercise(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    workout_id = db.Column(db.Integer, db.ForeignKey('workout.id'), primary_key=True)
    order = db.Column(db.Integer, primary_key=True)
    exercise_id = db.Column(db.Integer, db.ForeignKey('exercises.id'))
    sets = db.relationship('Set', backref='exercise', lazy='dynamic')

    def __repr__(self):
        return '<Exercise %r>' % (self.id)

class ExerciseView(ModelView):
    form_columns = ['id', 'workout', 'order', 'exercise']

class Set(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    order = db.Column(db.Integer, primary_key=True)
    weight = db.Column(db.Numeric)
    reps = db.Column(db.Integer)
    exercise_id = db.Column(db.Integer, db.ForeignKey('exercise.id'))

    def __repr__(self):
        return '<Set %r>' % (self.id)

class SetView(ModelView):
    form_columns = ['id', 'order', 'weight', 'reps', 'exercise']

admin.add_view(ModelView(User, db.session))
admin.add_view(ModelView(Workout, db.session))
admin.add_view(ModelView(Exercises, db.session))
admin.add_view(ExerciseView(Exercise, db.session))
admin.add_view(SetView(Set, db.session))

if __name__ == '__main__':
    app.run(debug=True)