from django.contrib import admin
from .models import GratitudeEntry


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
