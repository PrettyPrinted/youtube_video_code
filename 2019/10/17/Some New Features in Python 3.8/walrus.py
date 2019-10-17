request = {'form' : {'username' : 'Anthony', 'password' : 'sec'}}
db = []

def process_form(request):
    #password = request['form'].get('password')

    if len(password := request['form'].get('password')) > 5:
        db.append(password)
        return 'Added user!'
    else:
        return 'Password is too short!'

print(process_form(request))
print(db)