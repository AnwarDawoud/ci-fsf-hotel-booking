# models.py
from django.conf import settings
import cloudinary.uploader
from django.contrib.auth.models import AbstractUser
from django.core.exceptions import ValidationError
from django.db import models
from cloudinary.models import CloudinaryField
from django.db.models import Avg
from django.utils.crypto import get_random_string
from django.utils import timezone
from .choices import RATING_CHOICES
from django.contrib.auth import get_user_model  # Add this import
  



class CustomUser(AbstractUser):
    profile_picture = models.ImageField(upload_to='profile_pics/', null=True, blank=True)
    is_hotel_manager = models.BooleanField(default=False)
    is_client_user = models.BooleanField(default=False)
    is_administrator = models.BooleanField(default=False)
    reset_token = models.CharField(max_length=255, null=True, blank=True)

    def __str__(self):
        return self.username
    
    def generate_reset_token(self):
        return get_random_string(length=32)

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
    rated_bookings = models.ManyToManyField('hotel_your_choice.Booking', related_name='rated_hotels', blank=True)

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
        
        
class Booking(models.Model):
    STATUS_ACTIVE = 'active'
    STATUS_CANCELED = 'canceled'
    STATUS_RESCHEDULED = 'rescheduled'

    STATUS_CHOICES = [
        (STATUS_ACTIVE, 'Booking Active'),
        (STATUS_CANCELED, 'Booking Canceled'),
        (STATUS_RESCHEDULED, 'Booking Rescheduled'),
    ]

    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    hotel = models.ForeignKey(Hotel, on_delete=models.CASCADE)
    check_in_date = models.DateField()
    check_out_date = models.DateField()
    guests = models.PositiveIntegerField()
    issued_date = models.DateField(auto_now_add=True)
    rating = models.PositiveIntegerField(null=True, blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default=STATUS_ACTIVE)
    canceled_by = models.ForeignKey(get_user_model(), on_delete=models.SET_NULL, null=True, blank=True, related_name='canceled_bookings')
    original_booking = models.ForeignKey('self', null=True, blank=True, on_delete=models.SET_NULL)

    def __str__(self):
        return self.display_status()

    def display_status(self):
        if self.status == self.STATUS_ACTIVE:
            return f'{self.id} - {self.user.username} - {self.hotel.name} Booking (Active)'
        elif self.status == self.STATUS_CANCELED:
            canceled_by_display = f' by {self.canceled_by.username}' if self.canceled_by else ''
            return f'{self.id} - {self.user.username} - {self.hotel.name} Booking (Canceled{canceled_by_display})'
        elif self.status == self.STATUS_RESCHEDULED:
            if self.original_booking:
                return f'{self.id} - {self.user.username} - {self.hotel.name} Booking (Rescheduled from Booking ID#{self.original_booking.id})'
            else:
                return f'{self.id} - {self.user.username} - {self.hotel.name} Booking (Rescheduled - Original Booking Missing)'
        else:
            return super().__str__()

    def calculate_average_rating(self):
        hotel_ratings = Rating.objects.filter(booking__hotel=self.hotel, booking__status=self.STATUS_ACTIVE)
        average_rating = hotel_ratings.aggregate(Avg('rating'))['rating__avg']

        self.hotel.average_rating = average_rating
        self.hotel.save()

    def clean(self):
        if self.check_in_date and self.check_in_date < timezone.now().date():
            raise ValidationError({'check_in_date': 'Check-in date cannot be backdated.'})

        if self.check_out_date and self.check_in_date and self.check_out_date <= self.check_in_date:
            raise ValidationError({'check_out_date': 'Check-out date must be after the check-in date.'})

        overlapping_bookings = Booking.objects.filter(
            hotel=self.hotel,
            check_in_date__lt=self.check_out_date,
            check_out_date__gt=self.check_in_date,
            status=self.STATUS_ACTIVE
        ).exclude(id=self.id)

        if overlapping_bookings.exists():
            raise ValidationError({'check_in_date': 'Overlapping bookings exist during new booking creation.'})

    def save(self, *args, **kwargs):
        self.full_clean()
        
        super().save(*args, **kwargs)

        if hasattr(self, 'ratings'):
            self.calculate_average_rating()

        if self.status == self.STATUS_CANCELED:
            if self.original_booking:
                try:
                    original_booking = Booking.objects.get(id=self.original_booking.id)
                    original_booking.status = self.STATUS_CANCELED
                    original_booking.canceled_by = self.canceled_by
                    original_booking.rating = None
                    original_booking.save()
                    print(f"Original Booking with ID {original_booking.id} canceled.")
                except Booking.DoesNotExist:
                    print("Original Booking does not exist.")
            else:
                print(f"Booking with ID {self.id} is an original booking and has been canceled.")

class UserActivity(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, null=True, blank=True)
    activity_description = models.CharField(max_length=255)
    timestamp = models.DateTimeField(auto_now_add=True, null=True, blank=True)

class UserRating(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, null=True, blank=True)
    rating = models.IntegerField()
    is_approved = models.BooleanField(default=False)
    timestamp = models.DateTimeField(auto_now_add=True, null=True, blank=True)

class Rating(models.Model):
    user = models.ForeignKey('CustomUser', on_delete=models.CASCADE)
    booking = models.ForeignKey('hotel_your_choice.Booking', on_delete=models.CASCADE, related_name='ratings')
    hotel = models.ForeignKey(Hotel, on_delete=models.CASCADE, default=None)  # Add default value here
    rating = models.IntegerField(choices=RATING_CHOICES)
    text = models.TextField(blank=True, null=True)
    timestamp = models.DateTimeField(default=timezone.now)

    class Meta:
        # Add a unique constraint to prevent multiple ratings for the same user and booking
        unique_together = ('user', 'booking')

    def __str__(self):
        return f"Rating for {self.booking} by {self.user.username}"

class Comment(models.Model):
    id = models.BigAutoField(primary_key=True)  # Add this line for an explicit ID field
    text = models.TextField()
    timestamp = models.DateTimeField(default=timezone.now)
    booking = models.ForeignKey(Booking, on_delete=models.CASCADE, related_name='comments', default=None, null=True, blank=True)
    dislikes_count = models.IntegerField(null=True, blank=True, default=0)
    likes_count = models.IntegerField(null=True, blank=True, default=0)
    
    # Add this line to create a ForeignKey relationship with the Rating model
    rating = models.ForeignKey('Rating', on_delete=models.CASCADE, related_name='comments', default=None, null=True, blank=True)

    def __str__(self):
        return f"Comment at {self.timestamp}"
