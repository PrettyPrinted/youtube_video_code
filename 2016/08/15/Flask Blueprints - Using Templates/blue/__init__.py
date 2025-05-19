from flask import Flask 

app = Flask(__name__)

from blue.api.routes import mod
from blue.site.routes import mod
from blue.admin.routes import mod

app.register_blueprint(site.routes.mod)
app.register_blueprint(api.routes.mod, url_prefix='/api')
app.register_blueprint(admin.routes.mod, url_prefix='/admin')