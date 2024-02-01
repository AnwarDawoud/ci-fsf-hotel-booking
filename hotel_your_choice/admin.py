from django.contrib import admin
from .models import CustomUser 
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import Group, Permission
from django.utils.html import format_html
from django.utils import timezone
from django.contrib.auth import get_user_model
import logging
from django.contrib.admin.models import LogEntry

User = get_user_model()

logger = logging.getLogger(__name__)

# Function to log admin activity
def log_admin_activity(modeladmin, request, queryset):
    for obj in queryset:
        message = f"Admin {request.user.username} performed action on {obj._meta.verbose_name} {obj} at {timezone.now()}"
        logger.info(message)
        LogEntry.objects.create(level='INFO', message=message)

log_admin_activity.short_description = "Log selected items"

# Custom Log Entry Admin class
from django.contrib.admin.models import LogEntry

class LogEntryAdmin(admin.ModelAdmin):
    list_display = ('display_level', 'message_display', 'formatted_timestamp')
    search_fields = ('change_message',)
    readonly_fields = ('formatted_timestamp',)

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
    display_level.short_description = 'Level'

    # Method to display log entry message
    def message_display(self, obj):
        return format_html("<pre>{}</pre>", obj.change_message)
    message_display.short_description = 'Message'

    # Method to format log entry timestamp
    def formatted_timestamp(self, obj):
        return obj.action_time.strftime('%Y-%m-%d %H:%M:%S')
    formatted_timestamp.short_description = 'Timestamp'

admin.site.register(LogEntry, LogEntryAdmin)

@admin.register(CustomUser)
class CustomUserAdmin(BaseUserAdmin):
    list_display = ('username', 'email', 'first_name', 'last_name', 'is_hotel_manager', 'is_client_user', 'is_administrator')

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
            'fields': ('username', 'email', 'password1', 'password2')}
        ),
    )

# Create or get groups
administrator_group, _ = Group.objects.get_or_create(name='Administrators')
hotel_managers_group, _ = Group.objects.get_or_create(name='Hotel Managers')
users_group, _ = Group.objects.get_or_create(name='Users')

# Get all permissions and assign them to the superuser
all_permissions = Permission.objects.all()
superuser = User.objects.filter(is_superuser=True).first()
superuser.user_permissions.set(all_permissions)
