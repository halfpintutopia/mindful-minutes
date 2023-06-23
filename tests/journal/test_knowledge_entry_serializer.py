from journal.serializers import KnowledgeEntrySerializer


def test_valid_note_serializer():
    """
    GIVEN a valid knowledge entry serializer
    WHEN the data us passed to the serializer
    THEN the serializer should be valid
    """
    valid_serializer_data = {
        "content": "Understand what 'hoisting' means in JavaScript"
    }
    serializer = KnowledgeEntrySerializer(data=valid_serializer_data)
    assert serializer.is_valid()
    assert serializer.validated_data == valid_serializer_data
    assert serializer.data == valid_serializer_data
    assert not serializer.errors


def test_invalid_missing_content_knowledge_entry_serializer():
    """
    GIVEN an invalid knowledge entry serializer with missing title
    WHEN the data is passed to the serializer
    THEN the serializer should be invalid
    """
    invalid_serializer_data = {}
    serializer = KnowledgeEntrySerializer(data=invalid_serializer_data)
    assert not serializer.is_valid()
    assert serializer.validated_data == {}
    assert serializer.data == invalid_serializer_data
    print("Errors:", serializer.errors)
    assert serializer.errors == {"content": ["This field is required."]}
