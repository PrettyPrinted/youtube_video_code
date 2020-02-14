from django.shortcuts import render

from .forms import ContactForm

def index(request):
    form = ContactForm()
    context = {'form' : form}
    return render(request, 'index.html', context)