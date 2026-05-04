from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User


class LoginForm(forms.Form):
    username = forms.CharField(label='Utilizador')
    password = forms.CharField(label='Password', widget=forms.PasswordInput)


class RegisterForm(UserCreationForm):
    email = forms.EmailField(required=True, label='Email')

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']


class MagicLinkForm(forms.Form):
    email = forms.EmailField(label='Email')