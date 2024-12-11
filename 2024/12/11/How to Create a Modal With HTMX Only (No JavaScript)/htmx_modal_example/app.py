from flask import Flask, render_template

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/modal")
def modal():
    return render_template("partials/modal.html")

@app.route("/null")
def null():
    return ""