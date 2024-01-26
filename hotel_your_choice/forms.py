# hotel_your_choice/forms.py

from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django import forms
from .models import Booking, CustomUser, Hotel, Comment, Rating, Amenity, Photo
from .choices import RATING_CHOICES  # Fix the import
from django.contrib.auth.forms import PasswordResetForm
from django.contrib.auth import get_user_model
from django.utils import timezone  
from django.core.exceptions import ValidationError
from multiupload.fields import MultiFileField
from django.shortcuts import get_object_or_404
from PIL import Image  # Make sure to import PIL


class ModifyBookingForm(forms.ModelForm):
    class Meta:
        model = Booking
        fields = '__all__'


# Modify YourBookingForm to handle rescheduling
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




from django import forms
from django.core.exceptions import ValidationError
from .models import Hotel, Photo


from cloudinary.models import CloudinaryField
from cloudinary.exceptions import Error as CloudinaryException


class MultiFileField(forms.FileField):
    def to_python(self, data):
        if data in self.empty_values:
            return None
        elif not isinstance(data, list):
            data = [data]  # Ensure data is a list
        return [super(MultiFileField, self).to_python(item) for item in data]


class HotelForm(forms.ModelForm):
    youtube_video_url = forms.URLField(label='YouTube Video URL', required=False)
    other_photos = MultiFileField(required=False)
    amenities = forms.CharField(label='Amenities', widget=forms.Textarea(attrs={'rows': 3}), required=False)
    new_amenity_text = forms.CharField(label='New Amenity', required=False)

    class Meta:
        model = Hotel
        exclude = ['rated_bookings']  # Ensure 'id' is not included here
        fields = ['name', 'description', 'address', 'night_rate', 'capacity', 'main_photo', 'youtube_video_url', 'amenities', 'other_photos']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 4}),
        }

    def clean_other_photos(self):
        print("Cleaning Other Photos...")
        other_photos = self.cleaned_data.get('other_photos')
        cleaned_photos = []

        if other_photos is None:
            other_photos = []  # Default value if other_photos is None

        print(f"Other photos received: {other_photos}")

        for photo in other_photos:
            try:
                with Image.open(photo) as img:
                    img.verify()

                # Append only verified photos to the list
                cleaned_photos.append(photo)
            except Exception as e:
                print(f'Error verifying photo: {e}')
                print(f'Problematic photo: {photo}')

        return cleaned_photos

    def clean_amenities(self):
        print("Cleaning Amenities...")
        amenities = self.cleaned_data.get('amenities', '')
        new_amenity_text = self.cleaned_data.get('new_amenity_text')
        if new_amenity_text:
            amenities = new_amenity_text
        return amenities

    def save(self, commit=True):
        hotel_instance = super().save(commit=False)

        # Handle existing photos during editing
        if hotel_instance.id:
            existing_photos = Photo.objects.filter(hotel=hotel_instance)
            hotel_instance.other_photos.set(existing_photos)

        if commit:
            hotel_instance.save()

        return hotel_instance



class CustomRegistrationForm(UserCreationForm):
    email = forms.EmailField(required=True)
    first_name = forms.CharField(max_length=30, required=True)
    last_name = forms.CharField(max_length=30, required=True)
    contact_number = forms.CharField(max_length=15, required=True)

    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'first_name', 'last_name', 'contact_number', 'password1', 'password2']


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
        fields = ['text', 'rating']  # Add or remove fields as needed

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['text'].widget = forms.Textarea(attrs={'rows': 3})  # Customize widget if needed

    def save(self, commit=True):
        instance = super().save(commit=False)
        instance.timestamp = timezone.now()  # Set the timestamp automatically
        if commit:
            instance.save()
        return instance


class RescheduleForm(forms.Form):
    new_check_in_date = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}))
    new_check_out_date = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}))


class CancelBookingForm(forms.Form):
    reason = forms.CharField(widget=forms.Textarea)


class CustomPasswordResetForm(forms.Form):
    username = forms.CharField(max_length=150, required=True)
    new_password = forms.CharField(widget=forms.PasswordInput, required=True)
