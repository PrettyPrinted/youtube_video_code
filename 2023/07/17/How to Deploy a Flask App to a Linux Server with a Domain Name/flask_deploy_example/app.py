from flask import Flask 

app = Flask(__name__)

@app.route('/')
def index():
    return '<h1>Deployed!</h1><style>body { display: flex; align-items: center; justify-content: center; height: 100vh; }</style>'