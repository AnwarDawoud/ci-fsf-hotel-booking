# forms
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.core.exceptions import ValidationError
from django.shortcuts import get_object_or_404
from django.utils import timezone
from .models import CustomUser, Group
from .choices import RATING_CHOICES

# from .models import MultiFileField # Unable to fix error


from PIL import Image
from cloudinary.models import CloudinaryField
from cloudinary.exceptions import Error as CloudinaryException


from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser, Group

from django.core.exceptions import ValidationError


from .models import (
    CustomUser,
    Role,
    Booking,
    CustomUser,
    Hotel,
    Comment,
    Rating,
    Amenity,
    Photo,
)


class CustomRegistrationForm(UserCreationForm):
    contact_number = forms.CharField(max_length=15, required=False)
    is_hotel_manager = forms.BooleanField(
        label="Register as Hotel Manager", required=False
    )
    is_client_user = forms.BooleanField(
        label="Register as Client User", required=False
    )

    class Meta:
        model = CustomUser
        fields = [
            "username",
            "email",
            "first_name",
            "last_name",
            "contact_number",
            "password1",
            "password2",
            "is_hotel_manager",
            "is_client_user",
        ]
        widgets = {
            "username": forms.TextInput(attrs={"autocomplete": "username"}),
        }

    def clean_contact_number(self):
        contact_number = self.cleaned_data.get("contact_number")
        # Add custom validation for the contact number field
        if contact_number and not contact_number.startswith("+"):
            raise ValidationError("Contact number must start with a '+'")

        return contact_number

    def clean(self):
        cleaned_data = super().clean()
        is_hotel_manager = cleaned_data.get("is_hotel_manager")
        is_client_user = cleaned_data.get("is_client_user")

        # Add custom validation for the role selection
        if is_hotel_manager and is_client_user:
            raise ValidationError(
                "You cannot select both 'Register as Hotel Manager'"
                "and 'Register as Client User'"
            )

        return cleaned_data


def save(self, commit=True):
    user = super(CustomRegistrationForm, self).save(commit=False)

    password1 = self.cleaned_data.get("password1")
    if password1:
        user.set_password(password1)

    is_hotel_manager = self.cleaned_data.get("is_hotel_manager", False)
    is_client_user = self.cleaned_data.get("is_client_user", False)

    group_name = "Hotel Managers" if is_hotel_manager else "Users"
    roles_names = ["Is hotel manager"] if is_hotel_manager else [
        "Is client user"
        ]
    group, created = Group.objects.get_or_create(name=group_name)

    user.is_hotel_manager = is_hotel_manager
    user.is_client_user = is_client_user
    user.save()

    # Clear existing roles and add new ones
    user.roles.clear()
    roles = [Role(name=role_name) for role_name in roles_names]
    user.roles.add(*roles)

    user.groups.add(group)

    return user


class CustomPasswordResetForm(forms.Form):
    username = forms.CharField(max_length=150, required=True)
    new_password = forms.CharField(widget=forms.PasswordInput, required=True)


# Hotel Manager Forms


class MultiFileField(forms.FileField):
    def to_python(self, data):
        if data in self.empty_values:
            return None
        elif not isinstance(data, list):
            data = [data]  # Ensure data is a list
        return [super(MultiFileField, self).to_python(item) for item in data]


class HotelForm(forms.ModelForm):
    youtube_video_url = forms.URLField(
        label="YouTube Video URL", required=False
    )
    other_photos = MultiFileField(required=False)
    amenities = forms.CharField(
        label="Amenities", widget=forms.Textarea(attrs={"rows": 3}),
        required=False
    )
    new_amenity_text = forms.CharField(label="New Amenity", required=False)

    class Meta:
        model = Hotel
        # exclude = ['rated_bookings']  # Ensure 'id' is not included here
        fields = [
            "name",
            "description",
            "address",
            "night_rate",
            "capacity",
            "main_photo",
            "youtube_video_url",
            "amenities",
            "other_photos",
        ]
        widgets = {
            "description": forms.Textarea(attrs={"rows": 4}),
        }

    def clean_other_photos(self):
        print("Cleaning Other Photos...")
        other_photos = self.cleaned_data.get("other_photos")
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
                print(f"Error verifying photo: {e}")
                print(f"Problematic photo: {photo}")

        return cleaned_photos

    def clean_amenities(self):
        print("Cleaning Amenities...")
        amenities = self.cleaned_data.get("amenities", "")
        new_amenity_text = self.cleaned_data.get("new_amenity_text")
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


# Clients Forms

# Modify YourBookingForm to handle rescheduling
class ModifyBookingForm(forms.ModelForm):
    class Meta:
        model = Booking
        fields = '__all__'


# Modify YourBookingForm to handle new and rescheduled bookings
class YourBookingForm(forms.ModelForm):
    class Meta:
        model = Booking
        fields = ['check_in_date', 'check_out_date', 'guests']
        widgets = {
            'check_in_date': forms.DateInput(attrs={'type': 'date'}),
            'check_out_date': forms.DateInput(attrs={'type': 'date'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['check_in_date'].input_formats = ['%Y-%m-%d']
        self.fields['check_out_date'].input_formats = ['%Y-%m-%d']

# class RatingForm(forms.Form):
# rating = forms.ChoiceField(label='Rating (1-5)', choices=[(str(i), str(i))
# for i in range(1, 6)], widget=forms.RadioSelect(attrs={'class': 'with-gap'}))
# text = forms.CharField(label='Rating Text',
# widget=forms.Textarea(attrs={'class': 'materialize-textarea'}),
# required=False)


class RatingForm(forms.Form):
    RATING_CHOICES = (
        ("1", "1"),
        ("2", "2"),
        ("3", "3"),
        ("4", "4"),
        ("5", "5"),
    )
    rating = forms.MultipleChoiceField(
        choices=RATING_CHOICES, widget=forms.CheckboxSelectMultiple
    )
    text = forms.CharField(widget=forms.Textarea, required=False)


class RescheduleForm(forms.Form):
    new_check_in_date = forms.DateField(
        widget=forms.DateInput(attrs={"type": "date"})
    )
    new_check_out_date = forms.DateField(
        widget=forms.DateInput(attrs={"type": "date"})
    )


class CancelBookingForm(forms.Form):
    reason = forms.CharField(widget=forms.Textarea)


# Common Forms


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ["text", "rating"]  # Add or remove fields as needed

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["text"].widget = forms.Textarea(
            attrs={"rows": 3}
        )  # Customize widget if needed

    def save(self, commit=True):
        instance = super().save(commit=False)
        instance.timestamp = timezone.now()  # Set the timestamp automatically
        if commit:
            instance.save()
        return instance

