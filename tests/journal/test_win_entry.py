import pytest

from django.contrib.auth import get_user_model

from journal.models import WinEntry

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
    GIVEN a win entry model
    WHEN creating a win entry
    THEN user should have successfully created a win entry
    """
    win_entry = WinEntry.objects.create(
        user=user,
        content="20 minutes of meditation."
    )
    win_entry.save()
    win_entries = WinEntry.objects.all()
    assert len(win_entries) == 1
    assert win_entries[0].user == user
    assert win_entries[0].content == "20 minutes of meditation."
    assert isinstance(
        win_entries[0].content, str) and win_entries[0].content is not None
