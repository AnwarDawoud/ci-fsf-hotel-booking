# hotels_booking/urls.py

from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls import handler403, handler404, handler500
from hotel_your_choice import views  

urlpatterns = [
    path('admin/', admin.site.urls),
    # Include other app-specific URL patterns here if needed
    path('', include('hotel_your_choice.urls')),
    # Include authentication URLs
    path('auth/', include('django.contrib.auth.urls')),
]

handler403 = 'hotel_your_choice.views.forbidden'
handler404 = 'hotel_your_choice.views.not_found'
handler500 = 'hotel_your_choice.views.server_error'