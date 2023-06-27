import pytest

from django.contrib.auth import get_user_model
from rest_framework.test import APIClient

from journal.models import AppointmentEntry

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
