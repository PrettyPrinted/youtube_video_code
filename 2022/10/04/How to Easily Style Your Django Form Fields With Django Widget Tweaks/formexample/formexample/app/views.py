from django.shortcuts import render

from .forms import MemberForm

def index(request):
    form = MemberForm()
    context = {'form': form}
    return render(request, 'index.html', context)
