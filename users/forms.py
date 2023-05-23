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

    def clean(self):
        cleaned_data = super().clean()
        email = cleaned_data.get('email')

        if User.objects.filter(email=email).exists():
            msg = 'A user with that email already exists.'
            self.add_error('email', msg)

        return self.cleaned_data


class UserChangeForm(BaseUserChangeForm):
    email = forms.EmailField(required=True)
    password = None

    class Meta:
        model = User
        fields = [
            'username', 'email'
        ]

    def clean(self):
        cleaned_data = super().clean()
        email = cleaned_data.get('email')
        username = self.cleaned_data['username']
        current_user = User.objects.filter(username=username).first()
        user_with_email = User.objects.filter(email=email).first()
        if user_with_email and user_with_email != current_user:
            msg = 'A user with that email already exists.'
            self.add_error('email', msg)

        return self.cleaned_data
