from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .forms import CustomUserCreationForm, CustomUserChangeForm
from .models import CustomUser, UserSettings


class CustomUserAdmin(UserAdmin):
    """
    Admin configuration for User model

    The class defines the display and behaviour of the User model
    """
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm
    model = CustomUser
    readonly_fields = ("last_login", "date_joined")
    list_display = ("email", "first_name", "last_name",
                    "is_active", "is_staff")
    list_filter = ("email", "first_name", "last_name", "is_active", "is_staff")
    fieldsets = (
        (None, {"fields": ("email", "first_name", "last_name", "password")}),
        ("Permissions", {"fields": ("is_staff",
         "is_active", "groups", "user_permissions")}),
        ("Tracking", {"fields": ("last_login", "date_joined")})
    )
    add_fieldsets = (
        (None, {
            "classes": ('wide',),
            "fields": (
                "email",
                "first_name",
                "last_name",
                "password1",
                "password2",
                "is_staff",
                "is_active",
                "groups",
                "user_permissions"
            )}
         ),
    )
    search_fields = ["email", "first_name", "last_name"]
    ordering = ("email",)


@admin.register(UserSettings)
class UserSettingsAdmin(admin.ModelAdmin):
    """
    Admin configuration for the UserSettings model

    The class defines the display and behaviour of the UserSettings model
    """
    readonly_fields = (
        "created_date",
        "updated_date"
    )
    list_display = (
        "user",
        "start_week_day",
        "morning_check_in",
        "evening_check_in"
    )
    fields = (
        "user",
        "start_week_day",
        "morning_check_in",
        "evening_check_in"
    )


admin.site.register(CustomUser, CustomUserAdmin)
