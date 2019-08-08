from django.shortcuts import render

def index(request):
    mydict = {'key1' : 'value1'}
    mylist = [1, 2, 3, 4]
    list_of_dictionaries = [{'user' : '832'}, {'user' : '3238'}, {'user' : '30293'}]
    mybool = True
    context = {'name' : 'Pretty Printed', 'mydict' : mydict, 'mylist' : mylist, 'mybool' : mybool, 'list_of_dictionaries' : list_of_dictionaries}
    return render(request, 'examples/index.html', context)

def profile(request, username):
    context = {'username' : username}
    return render(request, 'examples/profile.html', context)