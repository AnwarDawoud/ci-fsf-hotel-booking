from django.conf import settings
from django.contrib.auth import get_user_model  
from django.contrib.auth.models import AbstractUser, Group, Permission
from django.core.exceptions import ValidationError
from django.db import models
from django.db.models import Avg  
from django.utils import timezone
from django.utils.crypto import get_random_string
from django.contrib.auth.base_user import AbstractBaseUser


import cloudinary.uploader
from cloudinary.models import CloudinaryField

from .choices import RATING_CHOICES

from django.conf import settings

class CustomUser(AbstractUser):
    is_hotel_manager = models.BooleanField(default=False)
    is_client_user = models.BooleanField(default=False)
    is_administrator = models.BooleanField(default=True)
    groups = models.ManyToManyField(Group, related_name='customuser_groups', db_table='custom_user_groups')
    user_permissions = models.ManyToManyField(Permission, related_name='customuser_permissions', db_table='custom_user_user_permissions')
    profile_picture = models.ImageField(upload_to='profile_pics/', null=True, blank=True)
    reset_token = models.CharField(max_length=255, null=True, blank=True)
    contact_number = models.CharField(max_length=15, blank=True, null=True)
    roles = models.ManyToManyField('Role')  # Reference Role using string

    def __str__(self):
        return self.username

    def generate_reset_token(self):
        return get_random_string(length=32)

    class Meta:
        db_table = 'custom_user'

class Role(models.Model):  # Define Role class separately
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name



#Hotel Manager Codes
class HotelManager(models.Manager):
    pass

class PhotoManager(models.Manager):
    pass

class Amenity(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name

class Photo(models.Model):
    hotel = models.ForeignKey('hotel_your_choice.Hotel', on_delete=models.CASCADE)
    image = CloudinaryField('image', folder='hotel_your_choice/hotel_photos/')
    
    objects = PhotoManager()


class Hotel(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    address = models.CharField(max_length=255)
    night_rate = models.DecimalField(max_digits=10, decimal_places=2, default=0.0)
    capacity = models.IntegerField(null=True, blank=True)
    room_number = models.IntegerField(null=True, blank=True)
    main_photo = CloudinaryField('image', folder='hotel_your_choice/hotel_main_photos/')
    other_photos = models.ManyToManyField('Photo', related_name='hotel_photos', blank=True)
    amenities = models.CharField(max_length=255, blank=True, null=True)
    manager = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='hotels_as_manager')
    # rated_bookings = models.ManyToManyField('hotel_your_choice.Booking', related_name='rated_hotels', blank=True)

    def get_ratings(self):
        return Rating.objects.filter(booking__hotel=self)

    def save(self, *args, **kwargs):
        # Convert amenities list to a comma-separated string if it's a list
        if isinstance(self.amenities, list):
            self.amenities = ', '.join(self.amenities)

        # Upload main_photo to Cloudinary if not uploaded already
        if isinstance(self.main_photo, CloudinaryField) and not self.main_photo.public_id:
            try:
                response = cloudinary.uploader.upload(self.main_photo.path)
                self.main_photo.public_id = response['public_id']
                self.main_photo.save()
            except Exception as e:
                # Handle the Cloudinary upload exception
                raise e

        # Save the Hotel instance
        super().save(*args, **kwargs)

        # Upload other_photos to Cloudinary with folder specified
        for photo in self.other_photos.all():
            if isinstance(photo.image, CloudinaryField) and not photo.image.public_id:
                try:
                    response = cloudinary.uploader.upload(photo.image.path)
                    photo.image.public_id = response['public_id']
                    photo.image.save()
                except Exception as e:
                    # Handle the Cloudinary upload exception
                    raise e

    def __str__(self):
        return self.name

    objects = HotelManager()

    class Meta:
        verbose_name_plural = 'Hotels'