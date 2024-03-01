from django.contrib import admin
from .models import UserSettings


@admin.register(UserSettings)
class UserSettingsAdmin(admin.ModelAdmin):
    """
    Admin configuration for the UserSettings model

    The class defines the display and behaviour of the UserSettings model
    """
    
    model = UserSettings
    readonly_fields = ("created_on", "updated_on")
    list_display = (
        "user",
        "start_week_day",
        "morning_check_in",
        "evening_check_in",
    )
    fields = ("user", "start_week_day", "morning_check_in", "evening_check_in")
