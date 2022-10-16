from flask import Flask, url_for, redirect

app = Flask(__name__)

@app.route("/")
def index():
	return "The index"

@app.route("/first")
def first_route():
	return url_for('index')

@app.route("/second")
def second_route():
	return redirect(url_for('third_route', name='Anthony'))

@app.route("/third/<string:name>")
def third_route(name):
	return "The name is " + name

if __name__ == '__main__':
	app.run(debug=True) 
