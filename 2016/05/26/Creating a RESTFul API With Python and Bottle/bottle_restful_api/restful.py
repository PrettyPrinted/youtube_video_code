from bottle import run, get, post, request, delete

animals = [{'name' : 'Ellie', 'type' : 'Elephant'},
			{'name' : 'Python', 'type' : 'Snake'},
			{'name' : 'Zed', 'type' : 'Zebra'}]

@get('/animal')
def getAll():
	return {'animals' : animals}

@get('/animal/<name>')
def getOne(name):
	the_animal = [animal for animal in animals if animal['name'] == name]
	return {'animal' : the_animal[0]}

@post('/animal')
def addOne():
	new_animal = {'name' : request.json.get('name'), 'type' : request.json.get('type')}
	animals.append(new_animal)
	return {'animals' : animals}

@delete('/animal/<name>')
def removeOne(name):
	the_animal = [animal for animal in animals if animal['name'] == name]
	animals.remove(the_animal[0])
	return {'animals' : animals}

run(reloader=True, debug=True)