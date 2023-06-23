import pytest

from django.contrib.auth import get_user_model

from journal.models import IdeasEntry

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
def test_create_ideas_entry(user):
    """
    GIVEN a ideas entry model
    WHEN creating a ideas entry
    THEN user should have successfully created a ideas entry
    """
    ideas_entry = IdeasEntry.objects.create(
        user=user,
        content="20 minutes of meditation."
    )
    ideas_entry.save()
    ideas_entries = IdeasEntry.objects.all()
    assert len(ideas_entries) == 1
    assert ideas_entries[0].user == user
    assert ideas_entries[0].content == "20 minutes of meditation."
    assert isinstance(
        ideas_entries[0].content, str) and ideas_entries[0].content is not None
