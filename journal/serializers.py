from rest_framework import serializers
from django.contrib.auth import get_user_model

from .models import UserSettings, AppointmentEntry, TargetEntry, Note, \
    KnowledgeEntry, GratitudeEntry, WinEntry, IdeasEntry, ImprovementEntry, \
    EmotionEntry

User = get_user_model()


class CustomUserSerializer(serializers.ModelSerializer):
    """
    CustomUserSerializer is a ModelSerializer
    that converts CustomUser model to JSON representation and vice versa
    """
    active = serializers.BooleanField(source="is_active")
    start_week_day = serializers.IntegerField(
        source="usersettings.start_week_day")
    morning_check_in = serializers.TimeField(
        source="usersettings.morning_check_in")
    evening_check_in = serializers.TimeField(
        source="usersettings.evening_check_in")

    class Meta:
        """
        Metadata class for CustomUserSerializer

        Defines the model and fields to be serialized
        """
        model = User
        fields = ["id", "email", "first_name", "last_name",
                  "is_staff", "active", "is_superuser",
                  "start_week_day", "morning_check_in", "evening_check_in"]


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
        read_only_fields = ("id", "created_on", "updated_on",)


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


class NoteSerializer(serializers.ModelSerializer):
    """
    Serializer for Note model to convert it to JSON representation
    """
    user = serializers.PrimaryKeyRelatedField(read_only=True)
    created_on = serializers.DateTimeField(format="%Y-%m-%d", read_only=True)

    class Meta:
        """
        Metadata class for NoteSerializer

        Defines the model and fields to be serialized
        """
        model = Note
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
