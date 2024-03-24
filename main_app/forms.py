from django import forms
from .models import UserProfile
from django.contrib.auth.forms import PasswordChangeForm
from .models import Inventory

class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['email', 'name', 'address', 'city', 'province', 'postal_code']

    class ChangePasswordForm(PasswordChangeForm):
        pass

class InventoryForm(forms.ModelForm):
    class Meta:
        model = Inventory
        fields = ['product_id', 'name', 'quantity', 'description']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 3}),
        }