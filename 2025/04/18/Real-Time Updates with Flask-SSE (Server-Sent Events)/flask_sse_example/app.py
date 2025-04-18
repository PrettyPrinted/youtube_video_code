import click

from flask import Flask, render_template
from flask_sse import sse

app = Flask(__name__)
app.config["REDIS_URL"] = "redis://localhost"

app.register_blueprint(sse, url_prefix="/stream")

@app.route("/")
def index():
    return render_template("index.html")

@app.cli.command("update-votes")
@click.argument("purple")
@click.argument("orange")
def update_votes(purple=1, orange=1):
    sse.publish({"votes": [purple, orange]}, type="votes")