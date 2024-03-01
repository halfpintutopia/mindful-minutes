from django.contrib import admin
from .models import EmotionEntry


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


