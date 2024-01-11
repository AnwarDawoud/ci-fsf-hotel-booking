# hotel_your_choice/forms.py

from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django import forms
from .models import Booking, CustomUser, Hotel, Comment, Rating, Amenity, Photo
from .choices import RATING_CHOICES  # Fix the import
from django.contrib.auth.forms import PasswordResetForm
from django.contrib.auth import get_user_model

class ModifyBookingForm(forms.ModelForm):
    class Meta:
        model = Booking
        fields = ['check_in_date', 'check_out_date', 'guests']  # Add the fields you want to modify

class YourBookingForm(forms.ModelForm):
    reschedule_booking = forms.BooleanField(
        required=False,
        widget=forms.HiddenInput(),
        initial=False,
    )

    class Meta:
        model = Booking
        fields = ['hotel', 'check_in_date', 'check_out_date', 'guests', 'reschedule_booking']
        widgets = {
            'check_in_date': forms.DateInput(attrs={'type': 'date'}),
            'check_out_date': forms.DateInput(attrs={'type': 'date'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Specify the input format for date fields
        date_format = '%Y-%m-%d'
        self.fields['check_in_date'].input_formats = [date_format]
        self.fields['check_out_date'].input_formats = [date_format]



class HotelForm(forms.ModelForm):
    youtube_video_url = forms.URLField(label='YouTube Video URL', required=False)

    class Meta:
        model = Hotel
        fields = ['name', 'description', 'address', 'night_rate', 'main_photo', 'amenities', 'capacity']

        widgets = {
            'description': forms.Textarea(attrs={'rows': 4}),
            'amenities': forms.CheckboxSelectMultiple(),
        }

    

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

class UpdatePermissionsForm(forms.Form):
    user_id = forms.IntegerField()
    new_permissions = forms.CharField(max_length=255)

class DeleteUserForm(forms.Form):
    user_id = forms.IntegerField()

class ViewUserLogForm(forms.Form):
    log_user_id = forms.IntegerField()

class RatingForm(forms.Form):
    rating = forms.ChoiceField(choices=RATING_CHOICES, widget=forms.RadioSelect)
    text = forms.CharField(widget=forms.Textarea, required=False)


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['text']

    text = forms.CharField(max_length=255, required=False)  # Adjust max_length as needed



class RescheduleForm(forms.Form):
    new_check_in_date = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}))
    new_check_out_date = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}))

class CancelBookingForm(forms.Form):
    reason = forms.CharField(widget=forms.Textarea)    



class CustomPasswordResetForm(forms.Form):
    username = forms.CharField(max_length=150, required=True)
    new_password = forms.CharField(widget=forms.PasswordInput, required=True)