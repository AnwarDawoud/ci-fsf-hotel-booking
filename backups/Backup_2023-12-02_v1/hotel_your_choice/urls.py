# hotel_your_choice/urls.py

from django.urls import path
from .views import (
    view_hotels, hotel_manager_dashboard, add_hotel,
    manage_bookings, book_hotel, client_dashboard,
    rate_experience, system_overview, manage_users,
    troubleshoot, register_view, login_view,
    logout_view, password_reset_view, unsubscribe_view
)

app_name = 'hotel_your_choice'

urlpatterns = [
    # Common URLs
    path('view-hotels/', view_hotels, name='view_hotels'),

    # Hotel Manager URLs
    path('hotel-manager/dashboard/', hotel_manager_dashboard, name='hotel_manager_dashboard'),
    path('hotel-manager/add-hotel/', add_hotel, name='add_hotel'),
    path('hotel-manager/manage-bookings/', manage_bookings, name='manage_bookings'),

    # Client URLs
    path('client/book-hotel/<int:hotel_id>/', book_hotel, name='book_hotel'),
    path('client/dashboard/', client_dashboard, name='client_dashboard'),
    path('client/rate-experience/<int:booking_id>/', rate_experience, name='rate_experience'),

    # Site Administrator URLs
    path('site-administrator/system-overview/', system_overview, name='system_overview'),
    path('site-administrator/manage-users/', manage_users, name='manage_users'),
    path('site-administrator/troubleshoot/', troubleshoot, name='troubleshoot'),

    # Authentication and Authorization URLs
    path('register/', register_view, name='register'),
    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),
    path('password-reset/', password_reset_view, name='password_reset'),
    path('unsubscribe/', unsubscribe_view, name='unsubscribe'),
]
