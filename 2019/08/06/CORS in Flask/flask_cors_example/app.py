from flask import Flask, jsonify
from flask_cors import CORS, cross_origin

def create_app():
    app = Flask(__name__)
    #CORS(app)

    @app.route('/api')
    @cross_origin()
    def api():
        return jsonify({'data' : 'It is now working!'})

    return app