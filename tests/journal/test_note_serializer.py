from journal.serializers import NoteSerializer


def test_valid_note_serializer():
    """
    GIVEN a valid note serializer
    WHEN the data us passed to the serializer
    THEN the serializer should be valid
    """
    valid_serializer_data = {
        "content": "I must order 'Eloquent JavaScript'",
    }
    serializer = NoteSerializer(data=valid_serializer_data)
    assert serializer.is_valid()
    assert serializer.validated_data == valid_serializer_data
    assert serializer.data == valid_serializer_data
    assert not serializer.errors


def test_invalid_missing_content_note_serializer():
    """
    GIVEN an invalid note serializer with missing title
    WHEN the data is passed to the serializer
    THEN the serializer should be invalid
    """
    invalid_serializer_data = {}
    serializer = NoteSerializer(data=invalid_serializer_data)
    assert not serializer.is_valid()
    assert serializer.validated_data == {}
    assert serializer.data == invalid_serializer_data
    print("Errors:", serializer.errors)
    assert serializer.errors == {"content": ["This field is required."]}
