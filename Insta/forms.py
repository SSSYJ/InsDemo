from django import forms
from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm
from Insta.models import InsUser

class CustomUserCreationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = InsUser
        fields = ('username', 'email', 'profile_pic')