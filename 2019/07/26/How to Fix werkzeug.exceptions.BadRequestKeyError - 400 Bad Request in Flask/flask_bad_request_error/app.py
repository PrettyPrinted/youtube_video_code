from flask import Flask, request

app = Flask(__name__)

@app.route('/form', methods=['GET', 'POST'])
def form():
    if request.method == 'POST':
        print(request.form['location'])
        print(request.form.get('location'))
        
    return '''
        <form method="POST">
            Location: <input name="locations" type="text">
            <input type="submit">
        </form>
    '''