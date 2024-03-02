from django.contrib.auth import get_user_model
from rest_framework import serializers

from .models import AppointmentEntry

User = get_user_model()


class AppointmentEntrySerializer(serializers.ModelSerializer):
    """
    Serializer for AppointmentEntry model to convert it to JSON representation
    """

    user = serializers.PrimaryKeyRelatedField(read_only=True)
    created_on = serializers.DateTimeField(format="%Y-%m-%d", read_only=True)

    class Meta:
        """
        Metadata class for AppointmentEntrySerializer

        Defines the model and fields to be serialized
        """

        model = AppointmentEntry
        exclude = ("updated_on",)
        read_only_fields = ("id",)
