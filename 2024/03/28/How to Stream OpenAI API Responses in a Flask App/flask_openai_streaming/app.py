from flask import Flask, render_template, request 
from openai import OpenAI

client = OpenAI()

def create_app():
    app = Flask(__name__)

    @app.route("/")
    def index():
        return render_template("index.html")

    @app.route("/answer", methods=["GET", "POST"])
    def answer():
        data = request.get_json()
        message = data["message"]

        def generate():
            stream = client.chat.completions.create(
                model="gpt-4",
                messages=[{"role": "user", "content": message}],
                stream=True
            ) 

            for chunk in stream:
                if chunk.choices[0].delta.content is not None:
                    yield(chunk.choices[0].delta.content)

        return generate(), {"Content-Type": "text/plain"}

    return app