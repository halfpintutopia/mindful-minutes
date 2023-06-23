

import pytest

from django.contrib.auth import get_user_model

from journal.models import EmotionEntry

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
def test_create_emotion_entry(user):
    """
    GIVEN a emotion entry model
    WHEN creating a emotion entry
    THEN user should have successfully created a emotion entry
    """
    emotion_entry = EmotionEntry.objects.create(
        user=user,
        emotion="happy"
    )
    emotion_entry.save()
    emotion_entries = EmotionEntry.objects.all()
    assert len(emotion_entries) == 1
    assert emotion_entries[0].user == user
    assert emotion_entries[0].content == "happy"
    assert isinstance(
        emotion_entries[0].content, str) and emotion_entries[0].content is not None
