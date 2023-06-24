from datetime import date, time

import json
import pytest

from django.contrib.auth import get_user_model
from rest_framework.test import APIClient

from journal.models import AppointmentEntry

User = get_user_model()


@pytest.mark.django_db
def test_add_appointment():
    """
    GIVEN a Django application
    WHEN the user requests to add an appointment
    THEN check that the appointment is added
    """
    appointment_entry = AppointmentEntry.objects.all()
    assert len(appointment_entry) == 0

    user = User.objects.create_user(
        email="normal@user.com",
        password="abcdefghij123!+_",
        first_name="Normal",
        last_name="User"
    )

    client = APIClient()
    client.force_authenticate(user=user)


    appointment_data = {
        "title": "Dentist",
        "date": "2023-07-06",
        "time_from": "09:00:00",
        "time_until": "10:00:00",
        "user": user.id, 
    }

    res = client.post(
        "/api/appointments/",
        appointment_data,
        format="json"
    )

    assert res.status_code == 201
    assert res.data["user"] == user.id
    assert res.data["title"] == "Dentist"
    assert res.data["date"] == "2023-07-06"
    assert res.data["time_from"] == "09:00:00"
    assert res.data["time_until"] == "10:00:00"

    appointment_entries = AppointmentEntry.objects.all()
    assert len(appointment_entries) == 1
