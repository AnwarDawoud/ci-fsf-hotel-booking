# hotel_your_choice/admin.py

from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import Hotel, Booking, CustomUser

class CustomUserAdmin(BaseUserAdmin):
    list_display = ('username', 'email', 'is_hotel_manager', 'is_client_user', 'is_administrator')
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        ('Personal Info', {'fields': ('first_name', 'last_name', 'email', 'profile_picture')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('Roles', {'fields': ('is_hotel_manager', 'is_client_user', 'is_administrator')}),
        ('Important dates', {'fields': ('last_login', 'date_joined')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'email', 'password1', 'password2', 'is_staff', 'is_superuser', 'is_hotel_manager', 'is_client_user', 'is_administrator')}
        ),
    )

admin.site.register(Hotel)
admin.site.register(Booking)
admin.site.register(CustomUser, CustomUserAdmin)
