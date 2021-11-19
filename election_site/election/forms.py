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

class AddCandidateForm(forms.Form):
    rollno = forms.CharField(required=True)
    manifesto = forms.CharField(required=True)
    post_applied = forms.ModelChoiceField(queryset=Post.objects.all())

class AddPost(forms.Form):
    post_name = forms.CharField(required=True)
    desc = forms.CharField(required=True)

class AddPost(forms.Form):
    post_name = forms.CharField(required=True)
    desc = forms.CharField(required=True)

class SearchForm(forms.Form):
    username = forms.CharField(required=True)
    