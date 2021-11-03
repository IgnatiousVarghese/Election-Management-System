from django import forms
from .models import *

LOGIN_TYPE = [
    ('1', 'Voter'),
    ('2', 'Candidate'),
    ('3', 'Election Cordinator')
]

class LoginForm(forms.Form):
    login_type = forms.ChoiceField(
        choices=LOGIN_TYPE,
    )
    username = forms.CharField(required=True)
    password = forms.CharField(required=True)

class password_change(forms.Form):
    email = forms.EmailField(required=True)
