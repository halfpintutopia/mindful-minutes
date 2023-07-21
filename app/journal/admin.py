from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .forms import CustomUserChangeForm, CustomUserCreationForm
from .models import (AppointmentEntry, CustomUser, EmotionEntry,
                     GratitudeEntry, IdeasEntry, ImprovementEntry,
                     KnowledgeEntry, NoteEntry, TargetEntry, UserSettings,
                     WinEntry)


class CustomUserAdmin(UserAdmin):
    """
    Admin configuration for User model

    The class defines the display and behaviour of the User model
    """

    add_form = CustomUserCreationForm
    form = CustomUserChangeForm
    model = CustomUser
    readonly_fields = ("last_login", "date_joined")
    list_display = ("email", "first_name", "last_name", "is_active", "is_staff")
    list_filter = ("email", "first_name", "last_name", "is_active", "is_staff")
    fieldsets = (
        (None, {"fields": ("email", "first_name", "last_name", "password")}),
        (
            "Permissions",
            {"fields": ("is_staff", "is_active", "groups", "user_permissions")},
        ),
        ("Tracking", {"fields": ("last_login", "date_joined")}),
    )
    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": (
                    "email",
                    "first_name",
                    "last_name",
                    "password1",
                    "password2",
                    "is_staff",
                    "is_active",
                    "groups",
                    "user_permissions",
                ),
            },
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

    model = UserSettings
    readonly_fields = ("created_on", "updated_on")
    list_display = ("user", "start_week_day", "morning_check_in", "evening_check_in")
    fields = ("user", "start_week_day", "morning_check_in", "evening_check_in")


@admin.register(AppointmentEntry)
class AppointmentEntryAdmin(admin.ModelAdmin):
    """
    Admin configuration for the AppointmentEntry model

    The class defines the display and behaviour fo the AppointmentEntry model
    """

    readonly_fields = ("created_on", "updated_on")
    list_display = ("user", "title", "date", "time_from", "time_until")
    fieldsets = (
        ("Owner", {"fields": ("user",)}),
        ("Title", {"fields": ("title",)}),
        ("Date & Time", {"fields": ("date", "time_from", "time_until")}),
    )
    search_fields = ["user", "title", "date"]
    ordering = ("date",)


@admin.register(TargetEntry)
class TargetEntryAdmin(admin.ModelAdmin):
    """
    Admin configuration for the AppointmentEntry model

    The class defines the display and behaviour fo the AppointmentEntry model
    """

    readonly_fields = ("created_on", "updated_on")
    list_display = ("order", "title", "user")
    fields = (
        "order",
        "title",
        "user",
        "created_on",
        "updated_on",
    )
    search_fields = ["user", "title", "created_on"]
    list_filter = ("title", "created_on")
    ordering = ("created_on",)


@admin.register(NoteEntry)
class NoteAdmin(admin.ModelAdmin):
    """
    Admin configuration for the AppointmentEntry model

    The class defines the display and behaviour fo the AppointmentEntry model
    """

    readonly_fields = ("created_on", "updated_on")
    list_display = ("user", "content")
    fields = (
        "user",
        "content",
        "created_on",
        "updated_on",
    )
    search_fields = ["user", "content", "created_on"]
    ordering = ("created_on",)


@admin.register(KnowledgeEntry)
class KnowledgeEntryAdmin(admin.ModelAdmin):
    """
    Admin configuration for the AppointmentEntry model

    The class defines the display and behaviour fo the AppointmentEntry model
    """

    readonly_fields = ("created_on", "updated_on")
    list_display = ("user", "content")
    fields = (
        "user",
        "content",
        "created_on",
        "updated_on",
    )
    search_fields = ["user", "content", "created_on"]
    ordering = ("created_on",)


@admin.register(GratitudeEntry)
class GratitudeEntryAdmin(admin.ModelAdmin):
    """
    Admin configuration for the GratitudeEntry model

    The class defines the display and behaviour fo the GratitudeEntry model
    """

    readonly_fields = ("created_on", "updated_on")
    list_display = ("user", "content")
    fields = (
        "user",
        "content",
        "created_on",
        "updated_on",
    )
    search_fields = ["user", "content", "created_on"]
    ordering = ("created_on",)


@admin.register(WinEntry)
class WinEntryAdmin(admin.ModelAdmin):
    """
    Admin configuration for the WinEntry model

    The class defines the display and behaviour fo the WinEntry model
    """

    readonly_fields = ("created_on", "updated_on")
    list_display = ("user", "title")
    fields = (
        "user",
        "title",
        "created_on",
        "updated_on",
    )
    search_fields = ["user", "title", "created_on"]
    ordering = ("created_on",)


@admin.register(IdeasEntry)
class IdeasEntryAdmin(admin.ModelAdmin):
    """
    Admin configuration for the IdeasEntry model

    The class defines the display and behaviour fo the IdeasEntry model
    """

    readonly_fields = ("created_on", "updated_on")
    list_display = ("user", "content")
    fields = (
        "user",
        "content",
        "created_on",
        "updated_on",
    )
    search_fields = ["user", "content", "created_on"]
    ordering = ("created_on",)


@admin.register(ImprovementEntry)
class ImprovementEntryAdmin(admin.ModelAdmin):
    """
    Admin configuration for the ImprovementEntry model

    The class defines the display and behaviour fo the ImprovementEntry model
    """

    readonly_fields = ("created_on", "updated_on")
    list_display = ("user", "content")
    fields = (
        "user",
        "content",
        "created_on",
        "updated_on",
    )
    search_fields = ["user", "content", "created_on"]
    ordering = ("created_on",)


@admin.register(EmotionEntry)
class EmotionEntryAdmin(admin.ModelAdmin):
    """
    Admin configuration for the EmotionEntry model

    The class defines the display and behaviour fo the EmotionEntry model
    """

    readonly_fields = ("created_on", "updated_on")
    list_display = ("user", "emotion")
    fields = (
        "user",
        "emotion",
        "created_on",
        "updated_on",
    )
    search_fields = ["user", "emotion", "created_on"]
    ordering = ("created_on",)


admin.site.register(CustomUser, CustomUserAdmin)
