from journal.serializers import GratitudeEntrySerializer


def test_valid_note_serializer():
    """
    GIVEN a valid gratitude entry serializer
    WHEN the data us passed to the serializer
    THEN the serializer should be valid
    """
    valid_serializer_data = {
        "content": "I am healthy."
    }
    serializer = GratitudeEntrySerializer(data=valid_serializer_data)
    assert serializer.is_valid()
    assert serializer.validated_data == valid_serializer_data
    assert serializer.data == valid_serializer_data
    assert not serializer.errors


def test_invalid_missing_content_gratitude_entry_serializer():
    """
    GIVEN an invalid gratitude entry serializer with missing title
    WHEN the data is passed to the serializer
    THEN the serializer should be invalid
    """
    invalid_serializer_data = {}
    serializer = GratitudeEntrySerializer(data=invalid_serializer_data)
    assert not serializer.is_valid()
    assert serializer.validated_data == {}
    assert serializer.data == invalid_serializer_data
    print("Errors:", serializer.errors)
    assert serializer.errors == {"content": ["This field is required."]}
