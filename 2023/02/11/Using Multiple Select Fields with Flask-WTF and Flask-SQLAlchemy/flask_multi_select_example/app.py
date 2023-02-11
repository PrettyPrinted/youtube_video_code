from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import FlaskForm 
from wtforms_alchemy import QuerySelectMultipleField
from wtforms import widgets

db = SQLAlchemy()

class Parent(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))

    children = db.relationship("Child", secondary="parent_child", back_populates="parents")

class Child(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))

    parents = db.relationship("Parent", secondary="parent_child", back_populates="children")

    def __str__(self):
        return self.name

db.Table(
    "parent_child",
    db.Column("parent_id", db.ForeignKey("parent.id"), primary_key=True),
    db.Column("child_id", db.ForeignKey("child.id"), primary_key=True)
)

class QuerySelectMultipleFieldWithCheckboxes(QuerySelectMultipleField):
    widget = widgets.ListWidget(prefix_label=False)
    option_widget = widgets.CheckboxInput()

class MyForm(FlaskForm):
    choices = QuerySelectMultipleFieldWithCheckboxes("Choices")

def create_app():
    app = Flask(__name__)

    app.config["SECRET_KEY"] = "ZOhaXJ5lgGjfQCT5pyw3"
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///db.sqlite3"

    db.init_app(app)

    @app.route("/<parent_id>", methods=["POST", "GET"])
    def index(parent_id):
        parent = Parent.query.get(parent_id)
        form = MyForm(data={"choices": parent.children})
        form.choices.query = Child.query.all()
        

        if form.validate_on_submit():
            
            parent.children.clear()
            parent.children.extend(form.choices.data)
            db.session.commit()

        return render_template("index.html", form=form)

    return app