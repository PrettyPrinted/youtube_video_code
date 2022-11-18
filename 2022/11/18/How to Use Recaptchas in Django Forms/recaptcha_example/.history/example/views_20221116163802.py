from django.shortcuts import render, redirect

from .forms import ContactForm

def index(request):
    if request.method == "POST":
        form = ContactForm(request.POST)
        if form.is_valid():
            print("VALID!")
            print(form.cleaned_data["captcha"])
            return redirect("index")
        else:
            print("INVALID!")
    form = ContactForm()
    context = {"form": form}
    return render(request, 'index.html', context)
