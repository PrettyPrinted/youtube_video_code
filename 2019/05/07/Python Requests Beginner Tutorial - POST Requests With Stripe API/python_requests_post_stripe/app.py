from flask import Flask, render_template, request
import requests 

app = Flask(__name__)
app.config['DEBUG'] = True

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/charge', methods=['POST'])
def charge():
    api_key = 'sk_test_DDQi3ygoTgLQQss7H69zGnMx002ZcSeQIe'
    token = request.form.get('stripeToken')

    # todo: stripe stuff
    headers = {'Authorization' : f'Bearer {api_key}'}
    data = {
            'amount' : 19900, 
            'currency' : 'usd', 
            'description' : 'Another Charge', 
            'source' : token
        }

    r = requests.post('https://api.stripe.com/v1/charges', headers=headers, data=data)

    print(r.text)

    return 'Done'