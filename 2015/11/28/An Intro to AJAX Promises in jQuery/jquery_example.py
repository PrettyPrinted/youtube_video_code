from flask import Flask, render_template, jsonify
app = Flask(__name__)

@app.route("/", methods=["GET"])
def retrieve():
    return render_template('layout.html')

@app.route("/ajaxtest", methods=["POST"])
def ajax():
 return jsonify({'result' : 'AJAX CALL COMPLETE!'})

if __name__ ==  "__main__":
    app.run(debug=True)