from datetime import date

import pytest

from django.contrib.auth import get_user_model
from rest_framework.test import APIClient

from journal.models import AppointmentEntry

User = get_user_model()


@pytest.mark.django_db
def test_add_appointment(authenticated_user):
    """
    GIVEN a Django application
    WHEN the user requests to add an appointment
    THEN check that the appointment is added
    """
    appointment_entries = AppointmentEntry.objects.all()
    assert len(appointment_entries) == 0

    client, user = authenticated_user

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
def test_add_appointment_invalid_json(authenticated_user):
    """
    GIVEN a Django application
    WHEN the user requests to add an appointment with an invalid payload
    THEN the payload is not sent
    """
    appointment_entries = AppointmentEntry.objects.all()
    assert len(appointment_entries) == 0

    (client, *_) = authenticated_user

    res = client.post(
        "/api/appointments/",
        {},
        format="json"
    )
    assert res.status_code == 400

    appointment_entries = AppointmentEntry.objects.all()
    assert len(appointment_entries) == 0


@pytest.mark.django_db
def test_add_appointment_missing_title(authenticated_user):
    """
    GIVEN a Django application
    WHEN the user request to add an appointment with missing title
    THEN the payload is not sent
    """
    appointment_entries = AppointmentEntry.objects.all()
    assert len(appointment_entries) == 0

    client, user = authenticated_user

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
def test_get_single_appointment_entry(authenticated_user, add_appointment_entry):
    """
    GIVEN a Django application
    WHEN the user requests to retrieve an appointment
    THEN check that the appointment is retrieved
    """
    client, user = authenticated_user

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
def test_get_single_appointment_incorrect_id(authenticated_user):
    """
    GIVEN a Django application
    WHEN the user requests to retrieve an appointment with an incorrect id
    THEN check the appointment is not retrieved
    """
    client, user = authenticated_user

    invalid_id = "random"
    res = client.get(f"/api/appointments/id/{invalid_id}/")

    assert res.status_code == 404


@pytest.mark.django_db
def test_get_all_appointment_entries(authenticated_user, add_appointment_entry):
    """
    GIVEN a Django application
    WHEN the user requests to retrieve all appointments
    THEN check all appointments are retrieved
    """
    appointment_entries = AppointmentEntry.objects.all()
    assert len(appointment_entries) == 0

    client, user = authenticated_user

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

    appointment_entries = AppointmentEntry.objects.all()
    assert len(appointment_entries) == 2


@pytest.mark.django_db
def test_get_all_appointment_entries_by_date(authenticated_user, add_appointment_entry):
    """
    GIVEN a Django application
    WHEN the user requests to retrieve all appointments by date
    THEN check all appointments are retrieved
    """
    client, user = authenticated_user

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


@pytest.mark.django_db
def test_remove_appointment_entry(authenticated_user, add_appointment_entry):
    """
    GIVEN a Django application
    WHEN the user requests to remove an appointment
    THEN the appointment is removed
    """
    appointment_entries = AppointmentEntry.objects.all()
    assert len(appointment_entries) == 0

    client, user = authenticated_user

    appointment_entry = add_appointment_entry(
        title="Dentist",
        date="2023-07-06",
        time_from="09:00:00",
        time_until="10:00:00",
        user=user,
    )

    res = client.get(f"/api/appointments/id/{appointment_entry.id}/")
    assert res.status_code == 200
    assert res.data["title"] == "Dentist"

    res_delete = client.delete(f"/api/appointments/id/{appointment_entry.id}/")
    assert res_delete.status_code == 204

    res_retrieve = client.get(f"/api/appointments/")
    assert res_retrieve.status_code == 200
    assert len(res_retrieve.data) == 0

    assert not AppointmentEntry.objects.filter(id=appointment_entry.id).exists()

    appointment_entries = AppointmentEntry.objects.all()
    assert len(appointment_entries) == 0


@pytest.mark.django_db
@pytest.mark.parametrize("incorrect_id, status_code", [
    ["random", 404],
    [12574, 404],
    ["98", 404]
])
def test_remove_appointment_invalid_id(authenticated_user, incorrect_id, status_code):
    """
    GIVEN a Django application
    WHEN the user requests to remove an appointment with an invalid id
    THEN the appointment is not removed
    """
    appointment_entries = AppointmentEntry.objects.all()
    assert len(appointment_entries) == 0

    client, user = authenticated_user

    res = client.get(f"/api/appointments/id/{incorrect_id}/")
    assert res.status_code == status_code

    updated_appointment_entries = AppointmentEntry.objects.all()
    assert len(appointment_entries) == len(updated_appointment_entries)
    assert len(updated_appointment_entries) == 0


@pytest.mark.django_db
def test_update_appointment_entry(authenticated_user, add_appointment_entry):
    """
    GIVEN a Django application
    WHEN the user requests to update an appointment
    THEN the appointment is updated
    """
    appointment_entries = AppointmentEntry.objects.all()
    assert len(appointment_entries) == 0

    client, user = authenticated_user

    appointment_entry = add_appointment_entry(
        title="Dentist",
        date="2023-07-06",
        time_from="09:00:00",
        time_until="10:00:00",
        user=user,
    )

    res = client.put(
        f"/api/appointments/id/{appointment_entry.id}/",
        {
            "title": "Dentist",
            "date": "2023-07-06",
            "time_from": "10:00:00",
            "time_until": "11:00:00",
        },
        format="json"
    )

    assert res.status_code == 200
    assert res.data["time_from"] == "10:00:00"
    assert res.data["time_until"] == "11:00:00"

    res_check = client.get(f"/api/appointments/id/{appointment_entry.id}/")
    assert res_check.status_code == 200
    assert res.data["time_from"] == "10:00:00"
    assert res.data["time_until"] == "11:00:00"

    appointment_entries = AppointmentEntry.objects.all()
    assert len(appointment_entries) == 1


@pytest.mark.django_db
@pytest.mark.parametrize("incorrect_id, status_code", [
    ["random", 404],
    [12574, 404],
    ["98", 404]
])
def test_update_appointment_entry_incorrect_id(authenticated_user, incorrect_id, status_code):
    """
    GIVEN a Django application
    WHEN the user requests to update an appointment with an incorrect id
    THEN the appointment is not updated
    """
    (client, *_) = authenticated_user

    res = client.put(f"/api/appointments/id/{incorrect_id}/")

    assert res.status_code == status_code


@pytest.mark.django_db
@pytest.mark.parametrize("add_appointment_entry, payload, status_code", [
    ["add_appointment_entry", {}, 400],
    ["add_appointment_entry", {
        "title": "Dentist",
        "date": "2023-07-06",
        "time from": "09:00:00",
        "time until": "10:00:00",
    }, 400],
], indirect=["add_appointment_entry"])
def test_update_appointment_entry_invalid_json(
    authenticated_user,
    add_appointment_entry,
    payload,
    status_code
):
    """
    GIVEN a Django application
    WHEN the user requests to update an appointment with invalid JSON
    THEN the appointment is not updated
    """
    client, user = authenticated_user

    appointment_entry = add_appointment_entry(
        title="Dentist",
        date="2023-07-06",
        time_from="09:00:00",
        time_until="10:00:00",
        user=user,
    )

    res = client.put(
        f"/api/appointments/id/{appointment_entry.id}/",
        payload,
        format="json"
    )

    assert res.status_code == status_code
