from django import forms
from .models import *

LOGIN_TYPE = [
    ('1', 'Voter'),
    ('2', 'Candidate'),
    ('3', 'Election Cordinator')
]

ALL_POST = []
posts = Post.objects.all()
for post in posts:
    ALL_POST.append((post.id, post.post_name))

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