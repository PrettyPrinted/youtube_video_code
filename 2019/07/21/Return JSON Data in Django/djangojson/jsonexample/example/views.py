from django.http import JsonResponse
from django.shortcuts import render

def index(request):
    comments = [
        {'name' : 'John Smith',
        'username' : '@johnsmith',
        'text' : 'I agree!'},
        {'name' : 'Stacy Warner',
        'username' : '@stacy1994',
        'text' : 'OP, you are the best'}
    ]

    # context = {'comments' : comments}
    
    # return render(request, 'index.html', context)
    
    return JsonResponse({'comments' : comments})