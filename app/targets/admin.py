from django.contrib import admin

from .models import TargetEntry


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
