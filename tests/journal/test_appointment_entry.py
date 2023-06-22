from datetime import time

import pytest

from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError

from journal.models import AppointmentEntry

User = get_user_model()


@pytest.fixture
def user():
    """
    Fixture for creating a user object.
    """
    return User.objects.create_user(
        email="normal@user.com",
        password="abcdefghij123!+_",
        first_name="Normal",
        last_name="User"
    )


@pytest.mark.django_db
def test_create_appointment_entry(user):
    """
    GIVEN an appointment entry model
    WHEN creating an appointment entry
    THEN user should have successfully created an appointment entry
    """
    appointment_entry = AppointmentEntry.objects.create(
        user=user,
        title="Dentist",
        date="2023-07-06",
        time_from=time(10, 0),
        time_until=time(11, 0)
    )
    appointment_entry.save()
    appointment_entries = AppointmentEntry.objects.all()
    assert len(appointment_entries) == 1
    assert appointment_entries[0].user == user
    assert appointment_entries[0].title == "Dentist"
    assert appointment_entries[0].date == "2023-07-06"
    assert isinstance(
        appointment_entries[0].date, str) and appointment_entries[0].date is not None
    assert appointment_entries[0].time_from == time(10, 0)
    assert isinstance(appointment_entries[0].time_from,
                      time) and appointment_entries[0].time_from is not None
    assert appointment_entries[0].time_until == time(11, 0)
    assert isinstance(appointment_entries[0].time_until,
                      time) and appointment_entries[0].time_until is not None


@pytest.mark.django_db
def test_create_appointment_entry_from_until():
    """
    GIVEN an appointment entry model
    WHEN creating an appointment entry
    THEN a ValidationError is raised
    """
    with pytest.raises(ValidationError):
        AppointmentEntry.objects.create(
            user=user,
            title="Dentist",
            date="2023-07-06",
            time_from=time(10, 0),
            time_until=time(9, 0)
        )
