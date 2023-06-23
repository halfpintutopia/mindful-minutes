from journal.serializers import TargetSerializer


def test_valid_target_serializer():
    """
    GIVEN a valid target serializer
    WHEN the data us passed to the serializer
    THEN the serializer should be valid
    """
    valid_serializer_data = {
        "title": "Mediate for 20 minutes",
        "order": 1,
    }
    serializer = TargetSerializer(data=valid_serializer_data)
    assert serializer.is_valid()
    assert serializer.validated_data == valid_serializer_data
    assert serializer.data == valid_serializer_data
    assert not serializer.errors


def test_invalid_missing_title_target_serializer():
    """
    GIVEN an invalid target serializer with missing title
    WHEN the data is passed to the serializer
    THEN the serializer should be invalid
    """
    invalid_serializer_data = {
        "order": 1
    }
    serializer = TargetSerializer(data=invalid_serializer_data)
    assert not serializer.is_valid()
    assert serializer.validated_data == {}
    assert serializer.data == invalid_serializer_data
    print("Errors:", serializer.errors)
    assert serializer.errors == {"title": ["This field is required."]}
