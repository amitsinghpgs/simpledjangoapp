from django.contrib.auth.forms import UserCreationForm
from django.db import models
from django.forms import ModelForm
from django.contrib.auth.models import User
from django import forms


class SignupForm(UserCreationForm):
    email = forms.EmailField(label='Email', max_length=200, help_text='Required')

    class Meta:
        model = User
        fields = (
            'username',
            'email',
            'password1',
            'password2',
        )


class PasswordResetForm(ModelForm):
    email = forms.EmailField(label='Email', max_length=200, help_text='Required')

    class Meta:
        model = User
        fields = ('username', 'email')
