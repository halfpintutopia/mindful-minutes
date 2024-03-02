from django.contrib import admin

from .models import AppointmentEntry


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
