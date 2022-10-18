from flask import Flask 
from flask.ext.mysqldb import MySQL 

app = Flask(__name__)
app.config['MYSQL_HOST'] = 'sql3.freemysqlhosting.net'
app.config['MYSQL_USER'] = 'yourusername'
app.config['MYSQL_PASSWORD'] = 'mypassword'
app.config['MYSQL_DB'] = 'yourdatabasename'
mysql = MySQL(app)

@app.route('/')
def index():
	cur = mysql.connection.cursor()
	cur.execute('''SELECT data FROM example WHERE id = 1''')
	rv = cur.fetchall()
	return str(rv)

@app.route('/addone/<string:insert>')
def add(insert):
	cur = mysql.connection.cursor()
	cur.execute('''SELECT MAX(id) FROM example''')
	maxid = cur.fetchone() #(10,)
	cur.execute('''INSERT INTO example (id, data) VALUES (%s, %s)''', (maxid[0] + 1, insert))
	mysql.connection.commit()
	return "Done"

@app.route('/getall')
def getall():
	cur = mysql.connection.cursor()
	cur.execute('''SELECT * FROM example''')
	returnvals = cur.fetchall() #((1, "ID1"), (2, "ID2"),...)

	printthis = ""
	for i in returnvals:
		printthis += i + "<br>"

	return printthis



if __name__ == '__main__':
	app.run(debug=True)