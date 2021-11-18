from django import forms
from .models import *

LOGIN_TYPE = [
    ('1', 'Voter'),
    ('2', 'Candidate'),
    ('3', 'Election Cordinator')
]

###  
###  can't write function which takes input from DB coz
###  while making migration error appears.
###  

ALL_POST = [   
    ('1', 'SAC'),
    ('2', 'Mag'),
    ('3', 'Hostel')
]

class LoginForm(forms.Form):
    login_type = forms.ChoiceField(
        choices=LOGIN_TYPE,
    )
    username = forms.CharField(required=True)
    password = forms.CharField(required=True)

class password_change(forms.Form):
    email = forms.EmailField(required=True)

class AddCandidateForm(forms.Form):
    rollno = forms.CharField(required=True)
    manifesto = forms.CharField(required=True)
    post_applied = forms.ChoiceField(
        choices= ALL_POST,
    )

class AddPost(forms.Form):
    post_name = forms.CharField(required=True)
    desc = forms.CharField(required=True)

class AddPost(forms.Form):
    post_name = forms.CharField(required=True)
    desc = forms.CharField(required=True)

class SearchForm(forms.Form):
    username = forms.CharField(required=True)
    