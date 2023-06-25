import pytest

from django.contrib.auth import get_user_model

from journal.models import ImprovementEntry

User = get_user_model()


@pytest.fixture
def user():
    """
    Fixture for creating a user object
    """
    return User.objects.create_user(
        email="normal@user.com",
        password="abcdefghij123!+_",
        first_name="Normal",
        last_name="User"
    )


@pytest.mark.django_db
def test_create_improvement_entry(user):
    """
    GIVEN a improvement entry model
    WHEN creating a improvement entry
    THEN user should have successfully created a improvement entry
    """
    improvement_entry = ImprovementEntry.objects.create(
        user=user,
        content="Listen more, talk less."
    )
    improvement_entry.save()
    improvement_entries = ImprovementEntry.objects.all()
    assert len(improvement_entries) == 1
    assert improvement_entries[0].user == user
    assert (improvement_entries[0].content ==
            "Listen more, talk less.")
    assert isinstance(
        improvement_entries[0].content, str
    ) and improvement_entries[0].content is not None
