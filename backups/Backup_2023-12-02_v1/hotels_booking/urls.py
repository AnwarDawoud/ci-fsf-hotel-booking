from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from hotel_your_choice.views import home


urlpatterns = [
    path('admin/', admin.site.urls),
    path('hotel_your_choice/', include('hotel_your_choice.urls', namespace='hotel_your_choice')),
    path('', home, name='home'),
]

# Serve static files during development
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
