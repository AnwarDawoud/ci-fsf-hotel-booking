# hotels_booking/urls.py

from django.contrib import admin
from django.urls import path, include
from django.conf import settings

from django.shortcuts import render
from hotel_your_choice.views import not_found


urlpatterns = [
    path('admin/', admin.site.urls),
    # Include other app-specific URL patterns here if needed
    path('', include('hotel_your_choice.urls')),
    # Include authentication URLs
    path('auth/', include('django.contrib.auth.urls')),
    # Handle 404 errors
    path('404/', not_found, name='not_found'),
]

