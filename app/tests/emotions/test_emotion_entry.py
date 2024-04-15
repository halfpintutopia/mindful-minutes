import pytest

from emotions.models import EmotionEntry


@pytest.mark.django_db
def test_create_emotion_entry(custom_user):
    """
    GIVEN a emotion entry model
    WHEN creating a emotion entry
    THEN user should have successfully created a emotion entry
    """
    emotion_entry = EmotionEntry.objects.create(
        user=custom_user, emotion="okay"
    )
    emotion_entry.save()
    emotion_entries = EmotionEntry.objects.all()
    assert len(emotion_entries) == 1
    assert emotion_entries[0].user == custom_user
    assert emotion_entries[0].emotion == "okay"
    assert (
        isinstance(emotion_entries[0].emotion, str)
        and emotion_entries[0].emotion is not None
    )
