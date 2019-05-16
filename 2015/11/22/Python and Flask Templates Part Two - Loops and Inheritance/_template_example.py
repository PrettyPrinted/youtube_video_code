from flask import Flask, render_template
app = Flask(__name__)

@app.route("/", methods=["GET"])
def index():
	names = {'name' : 'Anthony'}
	items = [{'text' : 'First'}, {'text' : 'Second'}, {'text' : 'Third'}]
	return render_template("layout.html", names=names, language='Python', lang=False, framework='Flask', items=items)

if __name__ ==  "__main__":
    app.run(debug=True)
