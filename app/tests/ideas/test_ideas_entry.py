import pytest

from ideas.models import IdeasEntry


@pytest.mark.django_db
def test_create_ideas_entry(custom_user):
    """
    GIVEN an ideas entry model
    WHEN creating an ideas entry
    THEN user should have successfully created a ideas entry
    """
    ideas_entry = IdeasEntry.objects.create(
        user=custom_user, content="20 minutes of meditation."
    )
    ideas_entry.save()
    ideas_entries = IdeasEntry.objects.all()
    assert len(ideas_entries) == 1
    assert ideas_entries[0].user == custom_user
    assert ideas_entries[0].content == "20 minutes of meditation."
    assert (
        isinstance(ideas_entries[0].content, str)
        and ideas_entries[0].content is not None
    )
