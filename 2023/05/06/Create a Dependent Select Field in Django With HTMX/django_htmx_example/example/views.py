from django.shortcuts import render

from .forms import LocationForm
from .models import City 

def index(request):
    if request.method == "POST":
        form = LocationForm(request.POST)
        if form.is_valid():
            print(form.cleaned_data["country"])
            print(form.cleaned_data["city"])
        else:
            print(form.errors)
    else:
        form = LocationForm()
    return render(request, 'index.html', {"form": form})

def load_cities(request):
    country_id = request.GET.get("country")
    cities = City.objects.filter(country_id=country_id)
    return render(request, "city_options.html", {"cities": cities})