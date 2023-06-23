from rest_framework import serializers

from .models import UserSettings, AppointmentEntry, Target, Note, \
    KnowledgeEntry, GratitudeEntry, WinEntry


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
        fields = '__all__'
        read_only_fields = ("id", "user", "created_date", "updated_date",)


class AppointmentEntrySerializer(serializers.ModelSerializer):
    """
    Serializer for AppointmentEntry model to convert it to JSON representation
    """
    user = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        """
        Metadata class for AppointmentEntrySerializer

        Defines the model and fields to be serialized
        """
        model = AppointmentEntry
        fields = "__all__"
        read_only_fields = ("id", "user", "created_date", "updated_date",)


class TargetSerializer(serializers.ModelSerializer):
    """
    Serializer for Target model to convert it to JSON representation
    """
    user = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        """
        Metadata class for TargetSerializer

        Defines the model and fields to be serialized
        """
        model = Target
        fields = "__all__"
        read_only_fields = ("id", "user", "created_date", "updated_date",)


class NoteSerializer(serializers.ModelSerializer):
    """
    Serializer for Note model to convert it to JSON representation
    """
    user = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        """
        Metadata class for NoteSerializer

        Defines the model and fields to be serialized
        """
        model = Note
        fields = "__all__"
        read_only_fields = ("id", "user", "created_date", "updated_date",)


class KnowledgeEntrySerializer(serializers.ModelSerializer):
    """
    Serializer for KnowledgeEntry model to convert it to JSON representation
    """
    user = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        """
        Metadata class for KnowledgeEntrySerializer

        Defines the model and fields to be serialized
        """
        model = KnowledgeEntry
        fields = "__all__"
        read_only_fields = ("id", "user", "created_date", "updated_date",)


class GratitudeEntrySerializer(serializers.ModelSerializer):
    """
    Serializer for GratitudeEntry model to convert it to JSON representation
    """
    user = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        """
        Metadata class for GratitudeEntrySerializer

        Defines the model and fields to be serialized
        """
        model = GratitudeEntry
        fields = "__all__"
        read_only_fields = ("id", "user", "created_date", "updated_date",)

class WinEntrySerializer(serializers.ModelSerializer):
    """
    Serializer for WinEntry model to convert it to JSON representation
    """
    user = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        """
        Metadata class for WinEntrySerializer

        Defines the model and fields to be serialized
        """
        model = WinEntry
        fields = "__all__"
        read_only_fields = ("id", "user", "created_date", "updated_date",)
