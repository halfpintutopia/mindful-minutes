from journal.serializers import EmotionEntrySerializer


def test_valid_emotion_entry_serializer():
    """
    GIVEN a valid emotion entry serializer
    WHEN the data us passed to the serializer
    THEN the serializer should be valid
    """
    valid_serializer_data = {
        "emotion": "happy"
    }
    serializer = EmotionEntrySerializer(data=valid_serializer_data)
    assert serializer.is_valid()
    assert serializer.validated_data == valid_serializer_data
    assert serializer.data == valid_serializer_data
    assert not serializer.errors


def test_invalid_missing_content_emotion_entry_serializer():
    """
    GIVEN an invalid emotion entry serializer with missing content
    WHEN the data is passed to the serializer
    THEN the serializer should be invalid
    """
    invalid_serializer_data = {}
    serializer = EmotionEntrySerializer(data=invalid_serializer_data)
    assert not serializer.is_valid()
    assert serializer.validated_data == {}
    assert serializer.data == invalid_serializer_data
    assert serializer.errors == {"emotion": ["This field is required."]}
