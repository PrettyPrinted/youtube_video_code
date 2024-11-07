from flask import Flask 
from flask_sqlalchemy import SQLAlchemy 

db = SQLAlchemy()

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50))

def create_app():   
    app = Flask(__name__)
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///db.sqlite3"

    db.init_app(app)

    @app.route("/admin")
    def admin():
        return "Hello Admin!"

    @app.route("/main")
    def main():
        return "Hello World!"

    @app.cli.command("create")
    def create():
        print("Create command has run")

    return app