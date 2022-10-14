from flask import Flask 
from flask_sqlalchemy import SQLAlchemy 
import sshtunnel 

app = Flask(__name__)

if __name__ == '__main__':

    tunnel = sshtunnel.SSHTunnelForwarder(
        ('ssh.pythonanywhere.com'), ssh_username='yourusername', ssh_password='yourpythonanywherepassword',
        remote_bind_address=('yourusername.mysql.pythonanywhere-services.com', 3306)
    )

    tunnel.start()

    app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://yourusername:yourdatabasepassword@127.0.0.1:{}/yourusername$default'.format(tunnel.local_bind_port)

else:
    app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://yourusername.mysql.pythonanywhere-services.com'

db = SQLAlchemy(app)

class Test(db.Model):
    id = db.Column(db.Integer, primary_key=True)
