from django import forms

from captcha.fields import ReCaptchaField
from captcha.widgets import ReCaptchaV3

class ContactForm(forms.Form):
    name = forms.CharField()
    email = forms.EmailField()
    captcha = ReCaptchaField(widget=ReCaptchaV3)