from django import forms

from crispy_forms.helper import FormHelper
from crispy_bulma.layout import Layout, Field, Submit
from crispy_bulma.bulma import InlineRadios

def validate_field(value):
    if value != "python":
        raise forms.ValidationError("You must enter Python")

class ContactForm(forms.Form):
    DEPARTMENT_CHOICES = (
        ('', '---------'),
        ('1', 'Sales'),
        ('2', 'Support'),
        ('3', 'General'),
    )

    PREFERRED_CONTACT_CHOICES = (
        ('email', 'Email'),
        ('phone', 'Phone'),
    )

    name = forms.CharField(max_length=100, validators=[validate_field])
    email = forms.EmailField()
    phone = forms.CharField(max_length=100)
    department = forms.ChoiceField(choices=DEPARTMENT_CHOICES)
    preferred_contact = forms.ChoiceField(choices=PREFERRED_CONTACT_CHOICES, widget=forms.RadioSelect, initial='email')
    subject = forms.CharField(max_length=100)
    message = forms.CharField(widget=forms.Textarea)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_id = "myform"
        self.helper.form_method = "post"
        self.helper.form_class = "mt-5"
        self.helper.form_horizontal = True

        self.helper.layout = Layout(
            Field("name", placeholder="Name"),
            Field("email", placeholder="Email"),
            Field("phone", placeholder="Phone number"),
            "department",
            InlineRadios("preferred_contact"),
            Field("subject", placeholder="What's your message about?"),
            Field("message", placeholder="Write something...", rows="4", cols="20"),
            Submit("submit", "Send message", css_class="is-primary")
        )