#This file contains classes for getting inputs everywhere throughout the application.

from django import forms
from .models import *

LOGIN_TYPE = [
    ('1', 'Voter'),
    ('2', 'Candidate'),
    ('3', 'Election Cordinator')
]

class LoginForm(forms.Form):
    login_type = forms.ChoiceField(choices=LOGIN_TYPE, 
    widget=forms.Select(attrs={
        'class' : 'form-select',
    }))
    username = forms.CharField(label = 'Username',
    widget=forms.TextInput(attrs={
        'class': 'form-control',
        'placeholder': 'Rollno / Username',
    }))
    password = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'form-control',
        'placeholder': 'password',
    }))

class password_change(forms.Form):
    email = forms.EmailField(required=True, 
    widget=forms.EmailInput(attrs={
        'class': 'form-control',
        'placeholder': 'Email',
    }))

class AddCandidateForm(forms.Form):
    rollno = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'form-control',
        'placeholder': 'Rollno',
    }))
    post_applied = forms.ModelChoiceField(queryset=Post.objects.all(),
    widget=forms.Select(attrs={
        'class' : 'form-select',
    }))
    manifesto = forms.CharField(widget=forms.Textarea(attrs={
        'class': 'form-control',
        'placeholder': 'Rollno',
        'rows' : 10,
    }))

class AddPost(forms.Form):
    post_name = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'form-control',
        'placeholder': 'Post Name',
    }))
    desc = forms.CharField(widget=forms.Textarea(attrs={
        'class': 'form-control',
        'placeholder': 'Give a small Description',
    }))

class SearchForm(forms.Form):
    username = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'form-control',
        'placeholder': 'Enter candidate roll number',
    }))
    