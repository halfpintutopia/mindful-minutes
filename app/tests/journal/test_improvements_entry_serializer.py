import pytest

from journal.serializers import ImprovementEntrySerializer


@pytest.mark.django_db
def test_valid_improvement_entry_serializer():
    """
    GIVEN a valid improvement entry serializer
    WHEN the data us passed to the serializer
    THEN the serializer should be valid
    """
    valid_serializer_data = {"content": "Listen more, talk less."}
    serializer = ImprovementEntrySerializer(data=valid_serializer_data)
    assert serializer.is_valid()
    assert serializer.validated_data == valid_serializer_data
    assert serializer.data == valid_serializer_data
    assert not serializer.errors


@pytest.mark.django_db
def test_invalid_missing_content_improvement_entry_serializer():
    """
    GIVEN an invalid improvement entry serializer with missing content
    WHEN the data is passed to the serializer
    THEN the serializer should be invalid
    """
    invalid_serializer_data = {}
    serializer = ImprovementEntrySerializer(data=invalid_serializer_data)
    assert not serializer.is_valid()
    assert serializer.validated_data == {}
    assert serializer.data == invalid_serializer_data
    assert serializer.errors == {"content": ["This field is required."]}
