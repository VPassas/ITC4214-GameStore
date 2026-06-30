from django import forms
from django.contrib.auth.models import User


class ProfileForm(forms.ModelForm):
    """A ModelForm built from the User model which lets a user view and edit their own first name, last name and email"""
    class Meta:
        model = User
        fields = ["first_name", "last_name", "email"]
