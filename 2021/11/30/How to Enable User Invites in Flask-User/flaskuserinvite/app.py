from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy 
from flask_user import UserManager, UserMixin

db = SQLAlchemy()

class User(db.Model, UserMixin):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    active = db.Column('is_active', db.Boolean(), nullable=False, server_default='1')
    email = db.Column(db.String(255, collation='NOCASE'), nullable=False, unique=True)
    password = db.Column(db.String(255), nullable=False, server_default='')
    email_confirmed_at = db.Column(db.DateTime())


class UserInvitation(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(100))
    invited_by_user_id = db.Column(db.Integer, db.ForeignKey('users.id'))


def create_app():
    app = Flask(__name__)

    app.config['SECRET_KEY'] = 'Vurm8JZXOGyacwkaPZYxvsUKK30u2gCwKfH5WIHoc32PGSyb'
    app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///db.sqlite3"
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    app.config['USER_APP_NAME'] = "Flask-User Invite Example"
    app.config['USER_ENABLE_EMAIL'] = True
    app.config['USER_ENABLE_USERNAME'] = False
    app.config['USER_REQUIRE_RETYPE_PASSWORD'] = False
    
    app.config['USER_EMAIL_SENDER_NAME'] = app.config['USER_APP_NAME']
    app.config['USER_EMAIL_SENDER_EMAIL'] = "anthony@prettyprinted.com"
    
    app.config['MAIL_SERVER'] = 'smtp.fastmail.com'
    app.config['MAIL_PORT'] = 465
    app.config['MAIL_USERNAME'] = 'anthony@prettyprinted.com'
    app.config['MAIL_PASSWORD'] = 'yourpassword'
    app.config['MAIL_DEFAULT_SENDER'] = '"Anthony" <anthony@prettyprinted.com>'
    app.config['MAIL_USE_SSL'] = True
    app.config['MAIL_USE_TLS'] = False
    
    app.config['USER_ENABLE_INVITE_USER'] = True
    app.config['USER_REQUIRE_INVITATION'] = True

    db.init_app(app)
    with app.app_context():
        db.create_all()

    user_manager =  UserManager(app, db, User, UserInvitationClass=UserInvitation)

    @app.route('/')
    def home_page():
        return render_template('index.html')

    return app