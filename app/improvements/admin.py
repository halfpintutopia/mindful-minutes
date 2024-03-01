from django.contrib import admin
from .models import ImprovementEntry


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
