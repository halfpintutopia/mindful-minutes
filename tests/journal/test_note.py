import pytest

from django.contrib.auth import get_user_model

from journal.models import Note

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
def test_create_note(user):
    """
    GIVEN a note model
    WHEN creating a note
    THEN user should have successfully created a note
    """
    note = Note.objects.create(
        user=user,
        content="I have to order 'Eloquent JavaScript'",
    )
    note.save()
    notes = Note.objects.all()
    assert len(notes) == 1
    assert notes[0].user == user
    assert notes[0].content == "I have to order 'Eloquent JavaScript'"
    assert isinstance(notes[0].content, str) and notes[0].content is not None
