from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm as BaseUserCreationForm,\
    UserChangeForm as BaseUserChangeForm


class UserCreationForm(BaseUserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = [
            'username', 'email', 'password1', 'password2'
        ]


class UserChangeForm(BaseUserChangeForm):
    email = forms.EmailField(required=True)
    password = None

    class Meta:
        model = User
        fields = [
            'username', 'email'
        ]
