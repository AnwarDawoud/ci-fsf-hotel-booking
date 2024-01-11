# hotel_your_choice/forms.py

from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django import forms
from .models import CustomUser, Hotel

class YourBookingForm(forms.Form):
    hotel = forms.ModelChoiceField(queryset=Hotel.objects.all(), label='Select a Hotel')
    check_in = forms.DateField()
    check_out = forms.DateField()
    guests = forms.IntegerField()

class HotelForm(forms.ModelForm):
    class Meta:
        model = Hotel
        fields = ['name', 'description', 'address']

class CustomRegistrationForm(UserCreationForm):
    email = forms.EmailField(required=True)
    first_name = forms.CharField(max_length=30, required=True)
    last_name = forms.CharField(max_length=30, required=True)
    contact_number = forms.CharField(max_length=15, required=True)

    is_hotel_manager = forms.BooleanField(required=False)
    is_client_user = forms.BooleanField(required=False)
    is_administrator = forms.BooleanField(required=False)

    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'first_name', 'last_name', 'contact_number', 'password1', 'password2', 'is_hotel_manager', 'is_client_user', 'is_administrator']
