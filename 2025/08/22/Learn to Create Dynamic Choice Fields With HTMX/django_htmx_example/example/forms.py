from django import forms 

from .models import Country, City 

class LocationForm(forms.Form):
    country = forms.ModelChoiceField(queryset=Country.objects.all(),
        widget=forms.Select(attrs={"hx-get": "load_cities/", "hx-target": "#id_city"}))
    city = forms.ModelChoiceField(queryset=City.objects.none())

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        if "country" in self.data:
            country_id = int(self.data.get("country"))
            self.fields["city"].queryset = City.objects.filter(country_id=country_id)