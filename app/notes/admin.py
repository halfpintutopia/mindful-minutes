from django.contrib import admin

from .models import NoteEntry


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
