from flask import Flask, jsonify, request
from flask.views import MethodView

app = Flask(__name__)

languages = [{'name' : 'JavaScript'}, {'name' : 'Python'}, {'name' : 'Ruby'}]

def get_language(name):
    return [language for language in languages if language['name'] == name][0]

class Language(MethodView):
    def get(self, language_name):
        if language_name:
            return jsonify({'language' : get_language(language_name)})
        else:
            return jsonify({'languages': languages})

    def post(self):
        new_language_name = request.json['name']
        language = {'name' : new_language_name}
        languages.append(language)
        return jsonify({'language' : get_language(new_language_name)}), 201

    def put(self, language_name):
        language = get_language(language_name)

        new_language_name = request.json['name']
        language['name'] = new_language_name
        return jsonify({'language' : get_language(new_language_name)})

    def delete(self, language_name):
        language = get_language(language_name)
        languages.remove(language)
        return '', 204

language_view = Language.as_view('language_api')
app.add_url_rule('/language', methods=['POST'], view_func=language_view)
app.add_url_rule('/language', methods=['GET'], defaults={'language_name' : None}, view_func=language_view)
app.add_url_rule('/language/<language_name>', methods=['GET', 'PUT', 'DELETE'], view_func=language_view)