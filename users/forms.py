from django.contrib.auth.forms import UserCreationForm
from django.db import models
from django.forms.widgets import PasswordInput
from .models import GENDER, CustomUser
from django import forms 

class SignUpForm(UserCreationForm):

    class Meta:
        model = CustomUser
        fields = ('first_name', 'last_name', 'email', 'gender', 'user_picture')

