from django import forms

class EventForm(forms.Form):
    name = forms.CharField()
    event_date = forms.DateField()