# hotel_your_choice/models.py
from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils import timezone
from .choices import RATING_CHOICES  # Fix the import
from django.contrib.auth import get_user_model
from django.utils.crypto import get_random_string
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.db.models import Avg
from datetime import datetime

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


class Amenity(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class Photo(models.Model):
    image = models.ImageField(upload_to='hotel_photos/')
    hotel = models.ForeignKey('Hotel', on_delete=models.CASCADE)

class Hotel(models.Model):
    # Basic information
    name = models.CharField(max_length=255)
    description = models.TextField()
    address = models.CharField(max_length=255)

    # Pricing and availability
    night_rate = models.DecimalField(max_digits=10, decimal_places=2, default=0.0)

    # Additional details
    capacity = models.IntegerField(null=True, blank=True)
    room_number = models.IntegerField(null=True, blank=True)

    # Main photo and other photos
    main_photo = models.ImageField(upload_to='hotel_main_photos/')
    other_photos = models.ManyToManyField(Photo, related_name='hotel_photos', blank=True)
    # Amenities
    amenities = models.ManyToManyField(Amenity)

    # Manager
    manager = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    def __str__(self):
        return self.name
    
class Booking(models.Model):
    STATUS_CHOICES = [
        ('active', 'Booking Active'),
        ('canceled', 'Booking Canceled'),
        ('rescheduled', 'Booking Rescheduled'),
    ]

    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    hotel = models.ForeignKey(Hotel, on_delete=models.CASCADE, null=True)
    check_in_date = models.DateField()
    check_out_date = models.DateField()
    guests = models.PositiveIntegerField()
    issued_date = models.DateField(auto_now_add=True)
    rating = models.PositiveIntegerField(null=True, blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='active')

    canceled_by = models.ForeignKey(get_user_model(), on_delete=models.SET_NULL, null=True, blank=True, related_name='canceled_bookings')
    original_booking = models.ForeignKey('self', null=True, blank=True, on_delete=models.SET_NULL)

    def __str__(self):
        if self.status == 'active':
            return f'{self.id} - {self.user.username} - {self.hotel.name} Booking (Active)'
        elif self.status == 'canceled':
            canceled_by_display = f' by {self.canceled_by.username}' if self.canceled_by else ''
            return f'{self.id} - {self.user.username} - {self.hotel.name} Booking (Canceled{canceled_by_display})'
        elif self.status == 'rescheduled':
            if self.original_booking:
                return f'{self.id} - {self.user.username} - {self.hotel.name} Booking (Rescheduled from Booking ID#{self.original_booking.id})'
            else:
                return f'{self.id} - {self.user.username} - {self.hotel.name} Booking (Rescheduled - Original Booking Missing)'
        else:
            return super().__str__()

    def calculate_average_rating(self):
        hotel_ratings = Rating.objects.filter(booking__hotel=self.hotel, booking__status='active')
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
            status='active'
        ).exclude(id=self.id)

        if overlapping_bookings.exists():
            raise ValidationError({'check_in_date': 'Overlapping bookings exist during new booking creation.'})

    def save(self, *args, **kwargs):
        self.full_clean()
        
        super().save(*args, **kwargs)

        if hasattr(self, 'ratings'):
            self.calculate_average_rating()

        if self.status == 'canceled':
            if self.original_booking:
                try:
                    original_booking = Booking.objects.get(id=self.original_booking.id)
                    original_booking.status = 'canceled'
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
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    booking = models.ForeignKey(Booking, on_delete=models.CASCADE, related_name='ratings')
    rating = models.IntegerField(choices=RATING_CHOICES)
    text = models.TextField(blank=True, null=True)
    timestamp = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"Rating for {self.booking} by {self.user.username}"

class Comment(models.Model):
    text = models.TextField()
    timestamp = models.DateTimeField(default=timezone.now)
    booking = models.ForeignKey(Booking, on_delete=models.CASCADE, related_name='comments', default=None, null=True, blank=True)
    dislikes_count = models.IntegerField(null=True, blank=True, default=0)
    likes_count = models.IntegerField(null=True, blank=True, default=0)

    def __str__(self):
        return f"Comment at {self.timestamp}"
    
    