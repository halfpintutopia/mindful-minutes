from django.contrib import admin
from .models import WinEntry


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
