from flask import Flask

app = Flask(__name__)

request_state = ''

@app.before_request
def before_request():
    global request_state
    request_state += ' before'

@app.after_request
def after_request(resp):
    global request_state
    request_state += ' after'
    return resp

@app.teardown_request
def teardown_request(excep):
    global request_state
    request_state += ' teardown <br>'

@app.route('/')
def index():
    return 'Hello ' + request_state

if __name__ == '__main__':
    app.run(debug=True)