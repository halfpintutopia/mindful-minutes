import pytest

from journal.models import GratitudeEntry


@pytest.mark.django_db
def test_create_knowledge_entry(custom_user):
    """
    GIVEN a knowledge entry model
    WHEN creating a knowledge entry
    THEN user should have successfully created a knowledge entry
    """
    gratitude_entry = GratitudeEntry.objects.create(
        user=custom_user, content="I am healthy"
    )
    gratitude_entry.save()
    gratitude_entries = GratitudeEntry.objects.all()
    assert len(gratitude_entries) == 1
    assert gratitude_entries[0].user == custom_user
    assert gratitude_entries[0].content == "I am healthy"
    assert (
        isinstance(gratitude_entries[0].content, str)
        and gratitude_entries[0].content is not None
    )
