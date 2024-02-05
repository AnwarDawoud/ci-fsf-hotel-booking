# urls.py
from django.urls import path, include
from django.contrib import admin

from django.conf import settings
from django.conf.urls.static import static

from django.contrib.auth import views as auth_views
from django.contrib.auth.views import PasswordResetDoneView

from . import views
from .views import (
    CustomPasswordResetConfirmView,
    CustomPasswordResetView,
    add_comment,
    book_hotel,
    delete_comment,
    delete_experience,
    dislike_comment,
    like_comment,
    reschedule_booking,
    cancel_booking,
    generate_excel,
    manage_bookings,
    edit_hotel,
    delete_hotel,
)


# hotels_booking/hotel_your_choice/urls.py

app_name = "hotel_your_choice"

urlpatterns = [
    # Redirect the root path to view-hotels
    path("", views.view_hotels, name="home"),
    # Common User URLs
    path("view-hotels/", views.view_hotels, name="view_hotels"),
    path(
        "delete-experience/<int:booking_id>/",
        delete_experience,
        name="delete_experience",
    ),
    path("add-comment/<int:booking_id>/", add_comment, name="add_comment"),
    path("delete_comment/<int:comment_id>/", delete_comment, name="delete_comment"),
    path("like-comment/<int:comment_id>/", like_comment, name="like_comment"),
    path("dislike-comment/<int:comment_id>/", dislike_comment, name="dislike_comment"),
    # Authentication and Authorization URLs
    path(
        "auth/",
        include(
            [
                path("register/", views.register_view, name="register"),
                path("login/", views.login_view, name="login"),
                path("logout/", views.logout_view, name="logout"),
                path(
                    "password_reset/",
                    CustomPasswordResetView.as_view(),
                    name="password_reset",
                ),
                path("unsubscribe/", views.unsubscribe_view, name="unsubscribe"),
            ]
        ),
    ),
    # Hotel Manager URLs
    path(
        "hotel-manager/",
        include(
            [
                path(
                    "dashboard/",
                    views.hotel_manager_dashboard,
                    name="hotel_manager_dashboard",
                ),
                path("hotel-manager/add-hotel/", views.add_hotel, name="add_hotel"),
                path(
                    "hotel-manager/manage-bookings/",
                    manage_bookings,
                    name="manage_bookings",
                ),
                path(
                    "hotel-manager/manage-bookings/download/",
                    generate_excel,
                    name="download_excel",
                ),
                path(
                    "view-booking-details/<int:booking_id>/",
                    views.view_booking_details,
                    name="view_booking_details",
                ),
                path("edit-hotel/<int:hotel_id>/", edit_hotel, name="edit_hotel"),
                path("delete-hotel/<int:hotel_id>/", delete_hotel, name="delete_hotel"),
                # Add other hotel manager URLs as needed
            ]
        ),
    ),
    # Client URLs
    path(
        "client/",
        include(
            [
                path("dashboard/", views.client_dashboard, name="client_dashboard"),
                path(
                    "client/book-hotel/<int:hotel_id>/<str:hotel_name>/",
                    book_hotel,
                    name="book_hotel",
                ),
                path(
                    "client/hotel_your_choice/reschedule-booking/<int:booking_id>/",
                    reschedule_booking,
                    name="reschedule_booking",
                ),
                path(
                    "cancel-booking/<int:booking_id>/",
                    cancel_booking,
                    name="cancel_booking",
                ),
                path(
                    "rate-experience/<int:booking_id>/",
                    views.rate_experience,
                    name="rate_experience",
                ),
                path("view-ratings/", views.view_user_ratings, name="view_ratings"),
                # Add other client URLs as needed
            ]
        ),
    ),
    # Admin URLs
    path("admin/", admin.site.urls),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


# Serve static and media files during development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
