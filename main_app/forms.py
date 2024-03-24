from django import forms
from .models import UserProfile
from django.contrib.auth.forms import PasswordChangeForm

class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['email', 'name', 'address', 'city', 'province', 'postal_code']

    class ChangePasswordForm(PasswordChangeForm):
        pass