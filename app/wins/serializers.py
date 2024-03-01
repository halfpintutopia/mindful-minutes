from django.contrib.auth import get_user_model
from rest_framework import serializers

from .models import WinEntry

User = get_user_model()


class WinEntrySerializer(serializers.ModelSerializer):
    """
    Serializer for WinEntry model to convert it to JSON representation
    """
    
    user = serializers.PrimaryKeyRelatedField(read_only=True)
    created_on = serializers.DateTimeField(format="%Y-%m-%d", read_only=True)
    
    class Meta:
        """
        Metadata class for WinEntrySerializer

        Defines the model and fields to be serialized
        """
        
        model = WinEntry
        exclude = ("updated_on",)
        read_only_fields = ("id",)
