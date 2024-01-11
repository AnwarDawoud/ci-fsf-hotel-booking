# hotel_your_choice/models.py

from django.contrib.auth.models import AbstractUser, Group, Permission
from django.db import models
from django.conf import settings

class CustomUser(AbstractUser):
    profile_picture = models.ImageField(upload_to='profile_pics/', null=True, blank=True)
    is_hotel_manager = models.BooleanField(default=False)
    is_client_user = models.BooleanField(default=False)
    is_administrator = models.BooleanField(default=False)

    groups = models.ManyToManyField(
        Group,
        verbose_name='groups',
        blank=True,
        help_text='The groups this user belongs to.',
        related_name='customuser_set',
        related_query_name='user',
    )

    user_permissions = models.ManyToManyField(
        Permission,
        verbose_name='user permissions',
        blank=True,
        help_text='Specific permissions for this user.',
        related_name='customuser_set',
        related_query_name='user',
    )

    def __str__(self):
        return self.username


class Hotel(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    address = models.CharField(max_length=255)
    managers = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='managed_hotels', blank=True)

    def __str__(self):
        return self.name


class Room(models.Model):
    hotel = models.ForeignKey(Hotel, on_delete=models.CASCADE)
    room_number = models.CharField(max_length=10)
    capacity = models.IntegerField()

    def __str__(self):
        return f'{self.hotel.name} - Room {self.room_number}'


class Booking(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    hotel = models.ForeignKey(Hotel, on_delete=models.CASCADE, null=True)
    check_in_date = models.DateField()
    check_out_date = models.DateField()
    guests = models.PositiveIntegerField()
    issued_date = models.DateField(auto_now_add=True)
    rating = models.PositiveIntegerField(null=True, blank=True)

    def __str__(self):
        return f'{self.user.username} - {self.hotel.name} Booking'

    def save(self, *args, **kwargs):
        if not self.hotel_id:
            default_hotel_id = 1  # Replace with your default hotel ID
            self.hotel_id = default_hotel_id

        super().save(*args, **kwargs)
