from django.contrib import admin
from .models import IdeasEntry


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
