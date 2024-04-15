from django.contrib.auth import get_user_model
from rest_framework import serializers

from .models import UserSettings

User = get_user_model()


class UserSettingsSerializer(serializers.ModelSerializer):
    """
    Serializer for UserSetting model to convert it to JSON representation
    """

    # related field when read_only then ti is excluded from serialized output
    # and this error occurs:
    # AttributeError: 'collections.OrderedDict' object has no attribute 'user'
    user = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        """
        Metadata class for UserSettingSerializer

        Defines the model and fields to be serialized
        """

        model = UserSettings
        fields = [
            "user",
            "start_week_day",
            "morning_check_in",
            "evening_check_in",
        ]
        read_only_fields = (
            "id",
            "created_on",
            "updated_on",
        )


class CustomUserSerializer(serializers.ModelSerializer):
    """
    CustomUserSerializer is a ModelSerializer
    that converts CustomUser model to JSON representation and vice versa
    """

    user_settings = UserSettingsSerializer(required=False)

    class Meta:
        """
        Metadata class for CustomUserSerializer

        Defines the model and fields to be serialized
        """

        model = User
        fields = [
            "id",
            "email",
            "first_name",
            "last_name",
            "is_staff",
            "is_active",
            "is_superuser",
            "user_settings",
        ]

        extra_kwargs = {
            "first_name": {"required": True},
            "last_name": {"required": True},
        }
