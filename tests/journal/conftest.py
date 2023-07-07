import pytest

from faker import Faker

from django.contrib.auth import get_user_model
from rest_framework.test import APIClient

from journal.models import AppointmentEntry, TargetEntry, \
    NoteEntry, KnowledgeEntry, GratitudeEntry, WinEntry, \
    IdeasEntry, ImprovementEntry, EmotionEntry, UserSettings

# retrieves the current active user model,
# which is set as the default user model AUTH_USER_MODEL,
# as extended AbstractUser
User = get_user_model()
fake = Faker()


@pytest.fixture
def authenticated_user():
    """
    Fixture to create an authenticated user
    """
    email = fake.email()
    password = fake.password()
    first_name = fake.first_name()
    last_name = fake.last_name()

    user = User.objects.create_user(
        email=email,
        password=password,
        first_name=first_name,
        last_name=last_name
    )

    # Acts as a simulated web browser that allows
    # you to make requests to API endpoints and receive responses.
    client = APIClient()
    # Sets up the test client with an authenticated user,
    # then use the client to perform actions on behalf of the authenticated user
    client.force_authenticate(user=user)

    return client, user


@pytest.fixture
def custom_user():
    """
    Fixture for creating a user object.
    """
    email = fake.email()
    password = fake.password()
    first_name = fake.first_name()
    last_name = fake.last_name()

    return User.objects.create_user(
        email=email,
        password=password,
        first_name=first_name,
        last_name=last_name
    )


@pytest.fixture
def custom_super_user():
    """
    Fixture for creating a super user object
    """
    email = fake.email()
    password = fake.password()
    first_name = fake.first_name()
    last_name = fake.last_name()

    return User.objects.create_superuser(
        email=email,
        password=password,
        first_name=first_name,
        last_name=last_name
    )


@pytest.fixture(scope="function")
def add_custom_user():
    """
    Fixture to create a CustomUser object in the database
    """
    def _add_custom_user(email, password, first_name, last_name):
        user = User.objects.create_user(
            email=email,
            password=password,
            first_name=first_name,
            last_name=last_name
        )
        return user
    return _add_custom_user


@pytest.fixture(scope="function")
def add_user_settings():
    """
    Fixture to create UserSettings object in the database
    """
    def _add_user_settings(start_week_day, morning_check_in, evening_check_in, user):
        user_settings = UserSettings.objects.create(
            user=user,
            start_week_day=start_week_day,
            morning_check_in=morning_check_in,
            evening_check_in=evening_check_in
        )
        return user_settings
    return _add_user_settings


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
        target_entry = TargetEntry.objects.create(
            user=user,
            title=title,
            order=order
        )
        return target_entry
    return _add_target_entry


@pytest.fixture(scope="function")
def add_note_entry():
    """
    Fixture to crete an NoteEntry object in the database
    """
    def _add_note_entry(content, user):
        note_entry = NoteEntry.objects.create(
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
    def _add_win_entry(title, user):
        win_entry = WinEntry.objects.create(
            user=user,
            title=title
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
