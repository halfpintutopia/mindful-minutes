from django.contrib.auth import get_user_model
from rest_framework import serializers

from .models import TargetEntry

User = get_user_model()


class TargetEntrySerializer(serializers.ModelSerializer):
    """
    Serializer for TargetEntry model to convert it to JSON representation
    """

    user = serializers.PrimaryKeyRelatedField(read_only=True)
    created_on = serializers.DateTimeField(format="%Y-%m-%d", read_only=True)

    class Meta:
        """
        Metadata class for TargetEntrySerializer

        Defines the model and fields to be serialized
        """

        model = TargetEntry
        exclude = ("updated_on",)
        read_only_fields = ("id",)
