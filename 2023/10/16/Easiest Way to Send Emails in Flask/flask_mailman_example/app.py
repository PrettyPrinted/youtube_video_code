from flask import Flask 
from flask_mailman import Mail, EmailMessage

mail = Mail()

def create_app():
    app = Flask(__name__)
    app.config["MAIL_SERVER"] = ""
    app.config["MAIL_PORT"] = 465
    app.config["MAIL_USERNAME"] = ""
    app.config["MAIL_PASSWORD"] = ""
    app.config["MAIL_USE_TLS"] = False
    app.config["MAIL_USE_SSL"] = True

    mail.init_app(app)

    @app.route("/")
    def index():
        msg = EmailMessage(
            "Here's the title!",
            "Body of the email",
            "from@email.com",
            ["to@email.com"]
        )
        msg.send()
        return "Sent email..."

    return app
