import flask

app = flask.Flask(__name__)

@app.route('/')
def index():
    elements = [
        'First',
        'Second',
        'Third',
        'Fourth',
        'Fifth',
        'Sixth',
        'Seventh',
        'Eighth',
        'Ninth',
        'Tenth',
        'Eleventh',
        'Twelfth'
    ]
    return flask.render_template('index.html', elements=elements * 10)