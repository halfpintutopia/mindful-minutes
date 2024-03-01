import pytest
from django.contrib.auth import get_user_model
from faker import Faker
from rest_framework.test import APIClient

from appointments.models import AppointmentEntry


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
        last_name=last_name,
    )

    # Acts as a simulated web browser that allows
    # you to make requests to API endpoints and receive responses.
    client = APIClient()
    # Sets up the test client with an authenticated user,
    # then use the client to perform actions on behalf of the authenticated
    # user
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
        last_name=last_name,
    )


@pytest.fixture
def custom_super_user():
    """
    Fixture for creating a superuser object
    """
    email = fake.email()
    password = fake.password()
    first_name = fake.first_name()
    last_name = fake.last_name()

    return User.objects.create_superuser(
        email=email,
        password=password,
        first_name=first_name,
        last_name=last_name,
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
            last_name=last_name,
        )
        return user

    return _add_custom_user


@pytest.fixture(scope="function")
def add_user_settings():
    """
    Fixture to create UserSettings object in the database
    """

    def _add_user_settings(
        start_week_day, morning_check_in, evening_check_in, user
    ):
        user_settings = UserSettings.objects.create(
            user=user,
            start_week_day=start_week_day,
            morning_check_in=morning_check_in,
            evening_check_in=evening_check_in,
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
            time_until=time_until,
        )
        return appointment_entry

    return _add_appointment_entry

