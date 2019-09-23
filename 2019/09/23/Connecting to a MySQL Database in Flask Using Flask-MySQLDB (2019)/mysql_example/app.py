from flask import Flask 
from flask_mysqldb import MySQL 

app = Flask(__name__)

app.config['MYSQL_USER'] = 'sql3306103'
app.config['MYSQL_PASSWORD'] = '2rmGIbqsnj'
app.config['MYSQL_HOST'] = 'sql3.freemysqlhosting.net'
app.config['MYSQL_DB'] = 'sql3306103'
app.config['MYSQL_CURSORCLASS'] = 'DictCursor'

mysql = MySQL(app)

@app.route('/')
def index():
    cur = mysql.connection.cursor()
    #cur.execute('''CREATE TABLE example (id INTEGER, name VARCHAR(20))''')

    #cur.execute('''INSERT INTO example VALUES (1, 'Anthony')''')
    #cur.execute('''INSERT INTO example VALUES (2, 'Billy')''')
    #mysql.connection.commit()

    cur.execute('''SELECT * FROM example''')
    results = cur.fetchall()
    print(results)
    return str(results[1]['id'])