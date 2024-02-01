from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.core.exceptions import ValidationError
from django.shortcuts import get_object_or_404
from django.utils import timezone
from .models import CustomUser, Group
from .choices import RATING_CHOICES
from multiupload.fields import MultiFileField
from PIL import Image
from cloudinary.models import CloudinaryField
from cloudinary.exceptions import Error as CloudinaryException
from .models import Role

from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser, Group

from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.core.exceptions import ValidationError
from django.contrib.auth.models import Group
from .models import CustomUser, Role

class CustomRegistrationForm(UserCreationForm):
    contact_number = forms.CharField(max_length=15, required=False)
    is_hotel_manager = forms.BooleanField(label='Register as Hotel Manager', required=False)
    is_client_user = forms.BooleanField(label='Register as Client User', required=False)

    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'first_name', 'last_name', 'contact_number', 'password1', 'password2', 'is_hotel_manager', 'is_client_user']
        widgets = {
            'username': forms.TextInput(attrs={'autocomplete': 'username'}),
        }

    def clean_contact_number(self):
        contact_number = self.cleaned_data.get('contact_number')
        # Add custom validation for the contact number field
        if contact_number and not contact_number.startswith('+'):
            raise ValidationError("Contact number must start with a '+'")

        return contact_number

    def clean(self):
        cleaned_data = super().clean()
        is_hotel_manager = cleaned_data.get('is_hotel_manager')
        is_client_user = cleaned_data.get('is_client_user')

        # Add custom validation for the role selection
        if is_hotel_manager and is_client_user:
            raise ValidationError("You cannot select both 'Register as Hotel Manager' and 'Register as Client User'")

        return cleaned_data

    def save(self, commit=True):
        user = super().save(commit=False)

        password1 = self.cleaned_data.get('password1')
        if password1:
            user.set_password(password1)

        is_hotel_manager = self.cleaned_data.get('is_hotel_manager', False)
        is_client_user = self.cleaned_data.get('is_client_user', False)

        group_name = 'Hotel Managers' if is_hotel_manager else 'Users'
        roles_names = ['Is hotel manager'] if is_hotel_manager else ['Is client user']

        group, created = Group.objects.get_or_create(name=group_name)

        user.is_hotel_manager = is_hotel_manager
        user.is_client_user = is_client_user
        user.save()

        # Clear existing roles and add new ones
        user.roles.clear()
        roles = [Role.objects.get_or_create(name=role_name)[0] for role_name in roles_names]
        user.roles.add(*roles)

        user.groups.add(group)

        return user
    
    
class CustomPasswordResetForm(forms.Form):
    username = forms.CharField(max_length=150, required=True)
    new_password = forms.CharField(widget=forms.PasswordInput, required=True)