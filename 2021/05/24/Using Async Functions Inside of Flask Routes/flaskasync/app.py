# Email validation: https://eva.pingutil.com/
# Address validation: https://www.lob.com
# Phone number validation: https://veriphone.io/

import asyncio
import httpx
import time

from auth import auth, APIKEY
from flask import Flask, render_template, request
from states import states

app = Flask(__name__)

@app.route('/sync', methods=['GET', 'POST'])
def sync_form():
    errors = {}
    if request.method == 'POST':
        start = time.time()

        if not request.form['firstName']:
            errors['firstName'] = 'First name is required.'
        
        if not request.form['lastName']:
            errors['lastName'] = 'Last name is required.'

        email_res = httpx.get(f'https://api.eva.pingutil.com/email?email={request.form["email"]}', timeout=None)

        if 'data' in email_res.json() and not email_res.json()['data']['deliverable']:
            errors['email'] = 'Invalid email address'

        data = {
            "primary_line" : request.form["address"],
            "secondary_line": request.form["address2"],
            "city" : request.form["city"],
            "state" : request.form["state"],
            "zip_code" : request.form["zip"]
        }

        address_res = httpx.post(f'https://api.lob.com/v1/us_verifications', auth=auth, data=data)
        if 'deliverability' in address_res.json() and not address_res.json()['deliverability'] == 'deliverable':
            errors['address'] = 'Invalid address'
            errors['address2'] = 'Invalid address'
            errors['city'] = 'Invalid city'
            errors['state'] = 'Invalid state'
            errors['zip'] = 'Invalid zip'

        phone_res = httpx.get(f'https://api.veriphone.io/v2/verify?key={APIKEY}&phone={request.form["phoneNumber"]}&default_country=US')

        if 'phone_valid' in phone_res.json() and not phone_res.json()['phone_valid']:
            errors['phoneNumber'] = 'Invalid phone number'

        end = time.time()
        print(end - start)

    return render_template('form.html', errors=errors, form=request.form, states=states)

@app.route('/async', methods=['GET', 'POST'])
async def async_form():
    errors = {}
    if request.method == 'POST':
        start = time.time()

        if not request.form['firstName']:
            errors['firstName'] = 'First name is required.'
        
        if not request.form['lastName']:
            errors['lastName'] = 'Last name is required.'

        data = {
            "primary_line" : request.form["address"],
            "secondary_line": request.form["address2"],
            "city" : request.form["city"],
            "state" : request.form["state"],
            "zip_code" : request.form["zip"]
        }

        async with httpx.AsyncClient() as client:
            email_res, address_res, phone_res = await asyncio.gather(
                client.get(f'https://api.eva.pingutil.com/email?email={request.form["email"]}', timeout=None),
                client.post(f'https://api.lob.com/v1/us_verifications', auth=auth, data=data),
                client.get(f'https://api.veriphone.io/v2/verify?key={APIKEY}&phone={request.form["phoneNumber"]}&default_country=US')
            )

        if 'data' in email_res.json() and not email_res.json()['data']['deliverable']:
            errors['email'] = 'Invalid email address'

        if 'deliverability' in address_res.json() and not address_res.json()['deliverability'] == 'deliverable':
            errors['address'] = 'Invalid address'
            errors['address2'] = 'Invalid address'
            errors['city'] = 'Invalid city'
            errors['state'] = 'Invalid state'
            errors['zip'] = 'Invalid zip'

        if 'phone_valid' in phone_res.json() and not phone_res.json()['phone_valid']:
            errors['phoneNumber'] = 'Invalid phone number'

        end = time.time()
        print(end - start)

    return render_template('form.html', errors=errors, form=request.form, states=states)