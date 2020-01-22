from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm


class SignUpForm(UserCreationForm):
    first_name = forms.CharField(max_length=100)
    last_name = forms.CharField(max_lemgth=100)
    email = forms.EmailField(max_length=200)


    class Meta:
        model = User
        fields = ('first_name', 'last_name' 'email', 'password1', 'password2', )
