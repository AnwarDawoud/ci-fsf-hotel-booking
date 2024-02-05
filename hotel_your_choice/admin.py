# Admin
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import Group, Permission
from django.utils.html import format_html
from django.utils import timezone
from django.contrib.auth import get_user_model
from django.db import models

from django.urls import reverse
from django.contrib.admin.models import LogEntry
from .models import Hotel, Booking, CustomUser, Rating, Amenity, Photo
# Custom Log Entry Admin class
from django.contrib.admin.models import LogEntry

import logging

User = get_user_model()

logger = logging.getLogger(__name__)


# Function to log admin activity
def log_admin_activity(modeladmin, request, queryset):
    for obj in queryset:
        message = f"Admin {request.user.username}"
        f"performed action on {obj._meta.verbose_name}"
        f"{obj} at {timezone.now()}"
        logger.info(message)
        LogEntry.objects.create(level="INFO", message=message)


log_admin_activity.short_description = "Log selected items"


class LogEntryAdmin(admin.ModelAdmin):
    list_display = ("display_level", "message_display", "formatted_timestamp")
    search_fields = ("change_message",)
    readonly_fields = ("formatted_timestamp",)

    # Method to display log entry level
    def display_level(self, obj):
        if obj.action_flag == 1:  # LogEntry.ADDITION
            return "Addition"
        elif obj.action_flag == 2:  # LogEntry.CHANGE
            return "Change"
        elif obj.action_flag == 3:  # LogEntry.DELETION
            return "Deletion"
        else:
            return "Unknown"

    display_level.short_description = "Level"

    # Method to display log entry message
    def message_display(self, obj):
        return format_html("<pre>{}</pre>", obj.change_message)

    message_display.short_description = "Message"

    # Method to format log entry timestamp
    def formatted_timestamp(self, obj):
        return obj.action_time.strftime("%Y-%m-%d %H:%M:%S")

    formatted_timestamp.short_description = "Timestamp"


admin.site.register(LogEntry, LogEntryAdmin)


@admin.register(CustomUser)
class CustomUserAdmin(BaseUserAdmin):
    list_display = (
        "username",
        "email",
        "first_name",
        "last_name",
        "is_hotel_manager",
        "is_client_user",
        "is_administrator",
    )

    fieldsets = (
        (None, {"fields": ("username", "password")}),
        (
                "Personal Info",
                {"fields": (
                    "first_name", "last_name", "email", "profile_picture"
                )}
            ),

        (
            "Permissions",
            {
                "fields": (
                    "is_active",
                    "is_staff",
                    "is_superuser",
                    "groups",
                    "user_permissions",
                )
            },
        ),
        (
            "Roles",
            {"fields": (
                "is_hotel_manager", "is_client_user", "is_administrator"
            )},
        ),
        ("Important dates", {"fields": ("last_login", "date_joined")}),
    )
    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": ("username", "email", "password1", "password2"),
            },
        ),
    )


# Create or get groups
administrator_group, _ = Group.objects.get_or_create(name="Administrators")
hotel_managers_group, _ = Group.objects.get_or_create(name="Hotel Managers")
users_group, _ = Group.objects.get_or_create(name="Users")

# Get all permissions and assign them to the superuser if it exists
all_permissions = Permission.objects.all()
superuser = User.objects.filter(is_superuser=True).first()
if superuser:
    superuser.user_permissions.set(all_permissions)


# Hotel Management
class RatingInline(admin.TabularInline):
    model = Rating
    extra = 0


class HotelAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "night_rate",
        "address",
        "display_amenities",
        "display_other_photos",
    )

    def display_amenities(self, obj):
        # Convert amenities string to a list for display
        return ", ".join(obj.amenities.split(", "))

    display_amenities.short_description = "Amenities"

    def display_other_photos(self, obj):
        return ", ".join(photo.image.url for photo in obj.other_photos.all())

    display_other_photos.short_description = "Other Photos"


def change_view(self, request, object_id, form_url="", extra_context=None):
    extra_context = extra_context or {}

    obj = self.get_object(request, object_id)
    if obj is not None:
        amenities_link = format_html(
            '<a href="{}?hotels__id__exact={}">{}</a>',
            reverse("admin:hotel_your_choice_amenity_changelist"),
            obj.id,
            obj.amenities,
        )

        extra_context["amenities_link"] = amenities_link
    return super(HotelAdmin, self).change_view(
        request, object_id, form_url, extra_context
    )


admin.site.register(Hotel, HotelAdmin)
admin.site.register(Amenity)


class PhotoAdmin(admin.ModelAdmin):
    list_display = ("hotel", "image")


admin.site.register(Photo, PhotoAdmin)


# Clients Admin


class BookingAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "user",
        "hotel",
        "check_in_date",
        "check_out_date",
        "booking_status_display",
    )
    list_filter = ("status", "hotel")
    search_fields = ("id", "user__username", "hotel__name")

    def booking_status_display(self, obj):
        if obj.status == "active":
            return format_html(
                '<span class="booking-active">Booking Active</span>'
            )
        elif obj.status == "canceled":
            canceled_by_display = (
                f" by {obj.canceled_by.username}"
                if obj.canceled_by else " by USER ID#"
            )
            return format_html(
                '<span class="booking-canceled">Booking Canceled{}</span>',
                canceled_by_display,
            )
        elif obj.status == "rescheduled":
            if obj.original_booking:
                original_booking = obj.original_booking
                return format_html(
                    '<span class="booking-rescheduled">' +
                    'Booking Rescheduled from ID#{0}</span>'
                    .format(original_booking.id)
                )
            else:
                return format_html(
                    '<span class="booking-rescheduled">' +
                    'Booking Rescheduled (Original Booking Missing)</span>'
                )
        else:
            return ""

    booking_status_display.short_description = "Booking Status"

    class Media:
        css = {
            "all": ("hotel_your_choice_css/admin_styles.css",),
        }


admin.site.register(Booking, BookingAdmin)


@admin.register(Rating)
class RatingAdmin(admin.ModelAdmin):
    list_display = ("user", "get_booking", "rating", "text", "timestamp")

    def get_booking(self, obj):
        return obj.booking

    get_booking.short_description = "Booking"


class ReschedulingStatusFilter(admin.SimpleListFilter):
    title = "Rescheduling Status"
    parameter_name = "rescheduling_status"

    def lookups(self, request, model_admin):
        return Booking.STATUS_CHOICES

    def queryset(self, request, queryset):
        if self.value():
            return queryset.filter(status=self.value())
        return queryset

