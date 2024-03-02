from django.contrib.auth import get_user_model
from rest_framework import serializers

from .models import KnowledgeEntry

User = get_user_model()


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
