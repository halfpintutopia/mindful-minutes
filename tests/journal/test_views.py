from datetime import date, time

import json
import pytest

from django.contrib.auth import get_user_model
from rest_framework.test import APIClient

from journal.models import AppointmentEntry

User = get_user_model()


@pytest.mark.django_db
def test_add_appointment(client):
    """
    GIVEN
    WHEN
    THEN
    """
    appointment_entry = AppointmentEntry.objects.all()
    assert len(appointment_entry) == 0

    user = User.objects.create_user(
        email="normal@user.com",
        password="abcdefghij123!+_",
        first_name="Normal",
        last_name="User"
    )

    # client = APIClient()
    # client.force_authenticate(user=user)

    res = client.post(
        "/api/appointments/",
        {
            "user": user.id,
            "title": "Dentist",
            "date": "2023-07-06",
            "time_from": "09:00:00",
            "time_until": "10:00:00",
        },
        format="json"
    )

    print("Response data:", res.data)

    assert res.status_code == 201
    assert res.data["title"] == "Dentist"
    assert res.data["date"] == "2023-07-06"
    assert res.data["time_from"] == "09:00:00"
    assert res.data["time_until"] == "10:00:00"

    appointment_entries = AppointmentEntry.objects.all()
    assert len(appointment_entries) == 1
