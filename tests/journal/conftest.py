import pytest

from django.contrib.auth import get_user_model
from rest_framework.test import APIClient

from journal.models import AppointmentEntry, Target, \
    Note, KnowledgeEntry, GratitudeEntry, WinEntry, \
    IdeasEntry, ImprovementEntry, EmotionEntry

User = get_user_model()


@pytest.fixture
def authenticated_user():
    """
    Fixture to create an authenticated user
    """
    user = User.objects.create_user(
        email="normal@user.com",
        password="abcdefghij123!+_",
        first_name="Normal",
        last_name="User"
    )

    # Acts as a simulatd web browser that allows
    # you to make requests to API endpoints and receive responses.
    client = APIClient()
    # Sets up the test client with an authenticated user,
    # then use the client to perform actions on behalf of the authenticated user
    client.force_authenticate(user=user)

    return client, user


@pytest.fixture(scope="function")
def add_appointment_entry():
    """
    Fixture to crete an AppointmentEntry object in the database
    """
    def _add_appointment_entry(title, date, time_from, time_until, user):
        appointment_entry = AppointmentEntry.objects.create(
            user=user,
            title=title,
            date=date,
            time_from=time_from,
            time_until=time_until
        )
        return appointment_entry
    return _add_appointment_entry


@pytest.fixture(scope="function")
def add_target_entry():
    """
    Fixture to crete an Target object in the database
    """
    def _add_target_entry(title, order, user):
        target_entry = Target.objects.create(
            user=user,
            title=title,
            order=order
        )
        return target_entry
    return _add_target_entry


@pytest.fixture(scope="function")
def add_note_entry():
    """
    Fixture to crete an Note object in the database
    """
    def _add_note_entry(content, user):
        note_entry = Note.objects.create(
            user=user,
            content=content,
        )
        return note_entry
    return _add_note_entry


@pytest.fixture(scope="function")
def add_knowledge_entry():
    """
    Fixture to crete an KnowledgeEntry object in the database
    """
    def _add_knowledge_entry(content, user):
        knowledge_entry = KnowledgeEntry.objects.create(
            user=user,
            content=content
        )
        return knowledge_entry
    return _add_knowledge_entry


@pytest.fixture(scope="function")
def add_gratitude_entry():
    """
    Fixture to crete an GratitudeEntry object in the database
    """
    def _add_gratitude_entry(content, user):
        gratitude_entry = GratitudeEntry.objects.create(
            user=user,
            content=content
        )
        return gratitude_entry
    return _add_gratitude_entry


@pytest.fixture(scope="function")
def add_win_entry():
    """
    Fixture to crete an WinEntry object in the database
    """
    def _add_win_entry(content, user):
        win_entry = WinEntry.objects.create(
            user=user,
            content=content
        )
        return win_entry
    return _add_win_entry


@pytest.fixture(scope="function")
def add_ideas_entry():
    """
    Fixture to crete an IdeasEntry object in the database
    """
    def _add_ideas_entry(content, user):
        ideas_entry = IdeasEntry.objects.create(
            user=user,
            content=content
        )
        return ideas_entry
    return _add_ideas_entry


@pytest.fixture(scope="function")
def add_improvement_entry():
    """
    Fixture to crete an ImprovementEntry object in the database
    """
    def _add_improvement_entry(content, user):
        improvement_entry = ImprovementEntry.objects.create(
            user=user,
            content=content
        )
        return improvement_entry
    return _add_improvement_entry


@pytest.fixture(scope="function")
def add_emotion_entry():
    """
    Fixture to crete an EmotionEntry object in the database
    """
    def _add_emotion_entry(emotion, user):
        emotion_entry = EmotionEntry.objects.create(
            user=user,
            emotion=emotion
        )
        return emotion_entry
    return _add_emotion_entry
