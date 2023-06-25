import pytest

from django.contrib.auth import get_user_model

from journal.models import GratitudeEntry

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
def test_create_knowledge_entry(user):
    """
    GIVEN a knowledge entry model
    WHEN creating a knowledge entry
    THEN user should have successfully created a knowledge entry
    """
    gratitude_entry = GratitudeEntry.objects.create(
        user=user,
        content="I am healthy"
    )
    gratitude_entry.save()
    gratitude_entries = GratitudeEntry.objects.all()
    assert len(gratitude_entries) == 1
    assert gratitude_entries[0].user == user
    assert gratitude_entries[0].content == "I am healthy"
    assert isinstance(
        gratitude_entries[0].content, str
    ) and gratitude_entries[0].content is not None
