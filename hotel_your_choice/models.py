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
