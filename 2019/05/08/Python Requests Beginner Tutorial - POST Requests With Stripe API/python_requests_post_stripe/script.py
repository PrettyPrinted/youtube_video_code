import requests, time
r = requests.post('https://pretty-printed-request-bin.herokuapp.com/qf1w1eqf', json={"ts":time.time(), 'hello' : 'Anthony'})
print(r.status_code)
print(r.content)