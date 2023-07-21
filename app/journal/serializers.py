from django.contrib.auth import get_user_model
from rest_framework import serializers

from .models import (AppointmentEntry, EmotionEntry, GratitudeEntry,
                     IdeasEntry, ImprovementEntry, KnowledgeEntry, NoteEntry,
                     TargetEntry, UserSettings, WinEntry)

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
        fields = ["user", "start_week_day", "morning_check_in", "evening_check_in"]
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


class NoteEntrySerializer(serializers.ModelSerializer):
    """
    Serializer for NoteEntry model to convert it to JSON representation
    """

    user = serializers.PrimaryKeyRelatedField(read_only=True)
    created_on = serializers.DateTimeField(format="%Y-%m-%d", read_only=True)

    class Meta:
        """
        Metadata class for NoteEntrySerializer

        Defines the model and fields to be serialized
        """

        model = NoteEntry
        exclude = ("updated_on",)
        read_only_fields = ("id",)


class KnowledgeEntrySerializer(serializers.ModelSerializer):
    """
    Serializer for KnowledgeEntry model to convert it to JSON representation
    """

    user = serializers.PrimaryKeyRelatedField(read_only=True)
    created_on = serializers.DateTimeField(format="%Y-%m-%d", read_only=True)

    class Meta:
        """
        Metadata class for KnowledgeEntrySerializer

        Defines the model and fields to be serialized
        """

        model = KnowledgeEntry
        exclude = ("updated_on",)
        read_only_fields = ("id",)


class GratitudeEntrySerializer(serializers.ModelSerializer):
    """
    Serializer for GratitudeEntry model to convert it to JSON representation
    """

    user = serializers.PrimaryKeyRelatedField(read_only=True)
    created_on = serializers.DateTimeField(format="%Y-%m-%d", read_only=True)

    class Meta:
        """
        Metadata class for GratitudeEntrySerializer

        Defines the model and fields to be serialized
        """

        model = GratitudeEntry
        exclude = ("updated_on",)
        read_only_fields = ("id",)


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


class IdeasEntrySerializer(serializers.ModelSerializer):
    """
    Serializer for IdeasEntry model to convert it to JSON representation
    """

    user = serializers.PrimaryKeyRelatedField(read_only=True)
    created_on = serializers.DateTimeField(format="%Y-%m-%d", read_only=True)

    class Meta:
        """
        Metadata class for IdeasEntrySerializer

        Defines the model and fields to be serialized
        """

        model = IdeasEntry
        exclude = ("updated_on",)
        read_only_fields = ("id",)


class ImprovementEntrySerializer(serializers.ModelSerializer):
    """
    Serializer for ImprovementEntry model to convert it to JSON representation
    """

    user = serializers.PrimaryKeyRelatedField(read_only=True)
    created_on = serializers.DateTimeField(format="%Y-%m-%d", read_only=True)

    class Meta:
        """
        Metadata class for ImprovementEntrySerializer

        Defines the model and fields to be serialized
        """

        model = ImprovementEntry
        exclude = ("updated_on",)
        read_only_fields = ("id",)


class EmotionEntrySerializer(serializers.ModelSerializer):
    """
    Serializer for EmotionEntry model to convert it to JSON representation
    """

    user = serializers.PrimaryKeyRelatedField(read_only=True)
    created_on = serializers.DateTimeField(format="%Y-%m-%d", read_only=True)

    class Meta:
        """
        Metadata class for ImprovementEntrySerializer

        Defines the model and fields to be serialized
        """

        model = EmotionEntry
        exclude = ("updated_on",)
        read_only_fields = ("id",)
