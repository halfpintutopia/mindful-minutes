from datetime import date

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
    appointment_entries = AppointmentEntry.objects.all()
    assert len(appointment_entries) == 0

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


@pytest.mark.django_db
def test_add_appointment_invalid_json():
    """
    GIVEN a Django application
    WHEN the user requests to add an appointment with an invalid payload
    THEN the payload is not sent
    """
    appointment_entries = AppointmentEntry.objects.all()
    assert len(appointment_entries) == 0

    user = User.objects.create_user(
        email="normal@user.com",
        password="abcdefghij123!+_",
        first_name="Normal",
        last_name="User"
    )

    client = APIClient()
    client.force_authenticate(user=user)

    res = client.post(
        "/api/appointments/",
        {},
        format="json"
    )
    assert res.status_code == 400

    appointment_entries = AppointmentEntry.objects.all()
    assert len(appointment_entries) == 0


@pytest.mark.django_db
def test_add_appointment_missing_title():
    """
    GIVEN a Django application
    WHEN the user request to add an appointment with missing title
    THEN the payload is not sent
    """
    appointment_entries = AppointmentEntry.objects.all()
    assert len(appointment_entries) == 0

    user = User.objects.create_user(
        email="normal@user.com",
        password="abcdefghij123!+_",
        first_name="Normal",
        last_name="User"
    )

    client = APIClient()
    client.force_authenticate(user=user)

    appointment_data = {
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

    assert res.status_code == 400

    appointment_entries = AppointmentEntry.objects.all()
    assert len(appointment_entries) == 0


@pytest.mark.django_db
def test_get_single_appointment_entry(add_appointment_entry):
    """
    GIVEN a Django application
    WHEN the user requests to retrieve an appointment
    THEN check that the appointment is retrieved
    """
    user = User.objects.create_user(
        email="normal@user.com",
        password="abcdefghij123!+_",
        first_name="Normal",
        last_name="User"
    )

    client = APIClient()
    client.force_authenticate(user=user)

    appointment = add_appointment_entry(
        title="Dentist",
        date="2023-07-06",
        time_from="09:00:00",
        time_until="10:00:00",
        user=user,
    )

    res = client.get(f"/api/appointments/id/{appointment.id}/")
    print("Response:", res)

    assert res.status_code == 200
    assert res.data["user"] == user.id
    assert res.data["title"] == "Dentist"
    assert res.data["time_from"] == "09:00:00"
    assert res.data["time_until"] == "10:00:00"


@pytest.mark.django_db
def test_get_single_appointment_incorrect_id():
    """
    GIVEN a Django application
    WHEN the user requests to retrieve an appointment with an incorrect id
    THEN check the appointment is not retrieved
    """
    user = User.objects.create_user(
        email="normal@user.com",
        password="abcdefghij123!+_",
        first_name="Normal",
        last_name="User"
    )

    client = APIClient()
    client.force_authenticate(user=user)

    invalid_id = "random"
    res = client.get(f"/api/appointments/id/{invalid_id}/")

    assert res.status_code == 404


@pytest.mark.django_db
def test_get_all_appointment_entries(add_appointment_entry):
    """
    GIVEN a Django application
    WHEN the user requests to retrieve all appointments
    THEN check all appointments are retrieved
    """
    user = User.objects.create_user(
        email="normal@user.com",
        password="abcdefghij123!+_",
        first_name="Normal",
        last_name="User"
    )

    client = APIClient()
    client.force_authenticate(user=user)

    add_appointment_entry(
        title="Dentist",
        date="2023-07-06",
        time_from="09:00:00",
        time_until="10:00:00",
        user=user,
    )

    add_appointment_entry(
        title="Gym",
        date="2023-07-06",
        time_from="19:00:00",
        time_until="20:00:00",
        user=user,
    )

    res = client.get("/api/appointments/")

    assert res.status_code == 200
    assert res.data[0]["title"] == "Dentist"
    assert res.data[1]["title"] == "Gym"


@pytest.mark.django_db
def test_get_all_appointment_entries_by_date(add_appointment_entry):
    """
    GIVEN a Django application
    WHEN the user requests to retrieve all appointments by date
    THEN check all appointments are retrieved
    """
    user = User.objects.create_user(
        email="normal@user.com",
        password="abcdefghij123!+_",
        first_name="Normal",
        last_name="User"
    )

    client = APIClient()
    client.force_authenticate(user=user)

    add_appointment_entry(
        title="Dentist",
        date="2023-07-06",
        time_from="09:00:00",
        time_until="10:00:00",
        user=user,
    )

    add_appointment_entry(
        title="Gym",
        date="2023-07-06",
        time_from="19:00:00",
        time_until="20:00:00",
        user=user,
    )

    add_appointment_entry(
        title="Lunch with Maria",
        date="2023-07-04",
        time_from="12:00:00",
        time_until="13:00:00",
        user=user,
    )

    add_appointment_entry(
        title="Cinema",
        date="2023-07-09",
        time_from="19:00:00",
        time_until="22:00:00",
        user=user,
    )

    current_date = date(2023, 7, 6)

    res = client.get(f"/api/appointments/date/{current_date}/")

    assert res.status_code == 200
    assert res.data[0]["date"] == "2023-07-06"
    assert res.data[0]["date"] == res.data[1]["date"]
    assert res.data[0]["title"] == "Dentist"
    assert res.data[1]["title"] == "Gym"

# @pytest.mark.django_db
# def test_remove_appointment(add_appointment_entry):
