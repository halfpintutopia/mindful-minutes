import pytest

from faker import Faker

from django.contrib.auth import get_user_model

from journal.serializers import NoteEntrySerializer
from journal.models import NoteEntry

User = get_user_model()
fake = Faker()


@pytest.mark.django_db
def test_valid_note_serializer():
    """
    GIVEN a valid note serializer
    WHEN the data us passed to the serializer
    THEN the serializer should be valid
    """
    email = fake.email()
    password = fake.password(length=16)
    first_name = fake.first_name()
    last_name = fake.last_name()

    user = User.objects.create_user(
        email=email,
        password=password,
        first_name=first_name,
        last_name=last_name
    )

    content = "I must order 'Eloquent JavaScript'"

    note_entry = NoteEntry.objects.create(
        user=user,
        content=content
    )

    serializer = NoteEntrySerializer(note_entry)
    deserialized_serializer = NoteEntrySerializer(data=serializer.data)
    assert deserialized_serializer.is_valid()

    assert deserialized_serializer["content"].value == content
    assert serializer.data.get("content") == content
    assert not deserialized_serializer.errors


def test_invalid_missing_content_note_serializer():
    """
    GIVEN an invalid note serializer with missing title
    WHEN the data is passed to the serializer
    THEN the serializer should be invalid
    """
    invalid_serializer_data = {}
    serializer = NoteEntrySerializer(data=invalid_serializer_data)
    assert not serializer.is_valid()
    assert serializer.validated_data == {}
    assert serializer.data == invalid_serializer_data
    assert serializer.errors == {"content": ["This field is required."]}
