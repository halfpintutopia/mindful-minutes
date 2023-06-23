from journal.serializers import IdeasEntrySerializer


def test_valid_ideas_entry_serializer():
    """
    GIVEN a valid ideas entry serializer
    WHEN the data us passed to the serializer
    THEN the serializer should be valid
    """
    valid_serializer_data = {
        "content": "I can discuss my design ideas with my cohort, arrange a good time to huddle in chat."
    }
    serializer = IdeasEntrySerializer(data=valid_serializer_data)
    assert serializer.is_valid()
    assert serializer.validated_data == valid_serializer_data
    assert serializer.data == valid_serializer_data
    assert not serializer.errors


def test_invalid_missing_content_ideas_entry_serializer():
    """
    GIVEN an invalid ideas entry serializer with missing content
    WHEN the data is passed to the serializer
    THEN the serializer should be invalid
    """
    invalid_serializer_data = {}
    serializer = IdeasEntrySerializer(data=invalid_serializer_data)
    assert not serializer.is_valid()
    assert serializer.validated_data == {}
    assert serializer.data == invalid_serializer_data
    print("Errors:", serializer.errors)
    assert serializer.errors == {"content": ["This field is required."]}
