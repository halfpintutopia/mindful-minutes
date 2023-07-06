import pytest

from journal.models import ImprovementEntry


@pytest.mark.django_db
def test_create_improvement_entry(custom_user):
    """
    GIVEN a improvement entry model
    WHEN creating a improvement entry
    THEN user should have successfully created a improvement entry
    """
    improvement_entry = ImprovementEntry.objects.create(
        user=custom_user,
        content="Listen more, talk less."
    )
    improvement_entry.save()
    improvement_entries = ImprovementEntry.objects.all()
    assert len(improvement_entries) == 1
    assert improvement_entries[0].user == custom_user
    assert (improvement_entries[0].content ==
            "Listen more, talk less.")
    assert isinstance(
        improvement_entries[0].content, str
    ) and improvement_entries[0].content is not None
