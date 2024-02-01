# hotels_booking/urls.py

from django.contrib import admin
from django.urls import path, include
from django.conf import settings

urlpatterns = [
    path('admin/', admin.site.urls),
    # Include other app-specific URL patterns here if needed
    path('', include('hotel_your_choice.urls')),
    # Include authentication URLs
    path('auth/', include('django.contrib.auth.urls')),
]