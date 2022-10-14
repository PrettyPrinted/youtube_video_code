import requests
from flask import Flask, render_template, request 

URL = 'https://api.fortnitetracker.com/v1/profile/pc/{}'
headers = {'TRN-Api-Key' : 'YOUR_API_KEY'}

#res = requests.get(URL, headers=headers)
#result = res.json()['lifeTimeStats']

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    player_one = None
    player_two = None
    player_one_stats = {}
    player_two_stats = {}

    if request.method == 'POST':
        player_one = request.form.get('playerOneName')

        if player_one:
            player_two = request.form.get('playerName')
        else:
            player_one = request.form.get('playerName')

        player_one_result = requests.get(URL.format(player_one), headers=headers).json()['lifeTimeStats']
        player_one_stats = populate_player_data(player_one_result)

        if player_two:
            player_two_result = requests.get(URL.format(player_two), headers=headers).json()['lifeTimeStats']
            player_two_stats = populate_player_data(player_two_result)

    return render_template('index.html', player_one=player_one, player_two=player_two,
        player_one_stats=player_one_stats, player_two_stats=player_two_stats)

def populate_player_data(api_data):

    temporary_dict = {}

    for r in api_data:
        if r['key'] == 'Wins':
            temporary_dict['wins'] = r['value']
        if r['key'] == 'Kills':
            temporary_dict['kills'] = r['value']
        if r['key'] == 'Matches Played':
            temporary_dict['matches'] = r['value']

    return temporary_dict

#print(populate_player_data(result))

if __name__ == '__main__':
    app.run(debug=True)