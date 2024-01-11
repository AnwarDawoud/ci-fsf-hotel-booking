# urls.py

from django.urls import path, include
from django.contrib import admin
from hotel_your_choice import views
from .views import CustomPasswordResetConfirmView, CustomPasswordResetView, delete_comment, reschedule_booking, cancel_booking
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views 
from django.contrib.auth.views import PasswordResetDoneView
from .views import view_hotels, generate_excel, manage_bookings

# hotels_booking/hotel_your_choice/urls.py

app_name = 'hotel_your_choice'

urlpatterns = [

    # Redirect the root path to view-hotels
    path('', views.view_hotels, name='home'),


    # Common User URLs
    
    path('delete-experience/<int:booking_id>/', views.delete_experience, name='delete_experience'),
    path('add-comment/<int:booking_id>/', views.add_comment, name='add_comment'),
    path('delete_comment/<int:comment_id>/', delete_comment, name='delete_comment'),
    path('like-comment/<int:comment_id>/', views.like_comment, name='like_comment'),
    path('dislike-comment/<int:comment_id>/', views.dislike_comment, name='dislike_comment'),
    path('view-hotels/', views.view_hotels, name='view_hotels'),

    # Hotel Manager URLs
    path('hotel-manager/', include([
        path('dashboard/', views.hotel_manager_dashboard, name='hotel_manager_dashboard'),
        path('hotel-manager/add-hotel/', views.add_hotel, name='add_hotel'),
        path('hotel-manager/manage-bookings/', manage_bookings, name='manage_bookings'),
        path('hotel-manager/manage-bookings/download/', generate_excel, name='download_excel'),
        path('view-booking-details/<int:booking_id>/', views.view_booking_details, name='view_booking_details'),
        
        # Add other hotel manager URLs as needed
    ])),

    # Client URLs
    path('client/', include([
        path('dashboard/', views.client_dashboard, name='client_dashboard'),
        path('book-hotel/<int:hotel_id>/', views.book_hotel, name='book_hotel'),
        path('client/hotel_your_choice/reschedule-booking/<int:booking_id>/', reschedule_booking, name='reschedule_booking'),
        path('cancel-booking/<int:booking_id>/', cancel_booking, name='cancel_booking'),
        path('rate-experience/<int:booking_id>/', views.rate_experience, name='rate_experience'),
        path('view-ratings/', views.view_user_ratings, name='view_ratings'),
        # Add other client URLs as needed
    ])),

    # Site Administrator URLs
    path('site-administrator/', include([
        path('system-overview/', views.system_overview, name='system_overview'),
        path('manage-users/', views.manage_users, name='manage_users'),
        path('troubleshoot/', views.troubleshoot, name='troubleshoot'),
        # Add other site administrator URLs as needed
    ])),

    # Authentication and Authorization URLs
    path('auth/', include([
        path('register/', views.register_view, name='register'),
        path('login/', views.login_view, name='login'),
        path('logout/', views.logout_view, name='logout'),
        path('password_reset/', CustomPasswordResetView.as_view(), name='password_reset'),
        path('unsubscribe/', views.unsubscribe_view, name='unsubscribe'),
    ])),
    
    # Admin URLs
    path('admin/', admin.site.urls),

    # Add API endpoints
    path('api/user_statistics/', views.get_analytics_data, name='user_statistics'),
   
    # Additional URLs for managing users (custom views from your existing views.py)
    path('api/user_data/', views.get_user_data, name='get_user_data'),
    path('api/update_permissions/<int:user_id>/', views.update_permissions, name='update_permissions'),
    path('api/delete_user/<int:user_id>/', views.delete_user, name='delete_user'),
    path('api/view_user_logs/<int:user_id>/', views.view_user_logs, name='view_user_logs'),
    path('api/add_user/', views.add_user, name='add_user'),
    path('api/approve_ratings/<int:rating_id>/', views.approve_ratings, name='approve_ratings'),
    path('api/view_user_ratings/<int:user_id>/', views.view_user_ratings, name='view_user_ratings'),
    path('api/user_activities/<int:user_id>/', views.load_user_activities, name='load_user_activities'),
    # Add other URL patterns as needed
    

    
    
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)