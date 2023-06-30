from datetime import date
# https://dennisokeeffe.medium.com/mocking-python-datetime-in-tests-with-freezegun-f5532307d6d6
# from freezegun import freeze_time

import pytest

from journal.models import AppointmentEntry


@pytest.mark.django_db
def test_add_appointment_entry(authenticated_user):
    """
    GIVEN a Django application
    WHEN the user requests to add an appointment
    THEN check that the appointment is added
    """
    appointment_entries = AppointmentEntry.objects.all()
    assert len(appointment_entries) == 0

    current_date = date.today()

    client, user = authenticated_user

    appointment_data = {
        "title": "Dentist",
        "date": current_date,
        "time_from": "09:00:00",
        "time_until": "10:00:00",
        "user": user.id,
    }

    res = client.post(
        f"/api/appointments/{current_date}/",
        appointment_data,
        format="json"
    )

    assert res.status_code == 201
    assert res.data["user"] == user.id
    assert res.data["title"] == "Dentist"
    assert res.data["date"] == str(current_date)
    assert res.data["time_from"] == "09:00:00"
    assert res.data["time_until"] == "10:00:00"

    appointment_entries = AppointmentEntry.objects.all()
    assert len(appointment_entries) == 1


@pytest.mark.django_db
@pytest.mark.parametrize("test_data", [
    {
        "payload": {},
        "status_code": 400
    },
    {
        "payload": {
            "title": "Dentist",
            "time from": "09:00:00",
            "time until": "10:00:00"
        },
        "status_code": 400
    }
])
def test_add_appointment_entry_incorrect_json(authenticated_user, test_data):
    """
    GIVEN a Django application
    WHEN the user requests to add an appointment with an invalid payload
    THEN the payload is not sent
    """
    appointment_entries = AppointmentEntry.objects.all()
    assert len(appointment_entries) == 0

    current_date = date.today()

    client, user = authenticated_user

    test_data["payload"]["date"] = current_date
    test_data["payload"]["user"] = user.id

    res = client.post(
        f"/api/appointments/{current_date}/",
        {},
        format="json"
    )
    assert res.status_code == 400

    appointment_entries = AppointmentEntry.objects.all()
    assert len(appointment_entries) == 0


@pytest.mark.django_db
@pytest.mark.parametrize("date_param", ["2023-07-01", "2023-06-20"])
def test_add_appointment_entry_not_current_date(
    authenticated_user,
    date_param
):
    """
    GIVEN a Django application
    WHEN the user attempts to add an appointment entry on a date,
    that is not the current date
    THEN the appointment entry is not created
    """
    appointment_entries = AppointmentEntry.objects.all()
    assert len(appointment_entries) == 0

    current_date = date.today()

    client, user = authenticated_user

    appointment_data = {
        "title": "Dentist",
        "date": current_date,
        "time_from": "09:00:00",
        "time_until": "10:00:00",
        "user": user.id,
    }

    res = client.post(
        f"/api/appointments/{date_param}/",
        appointment_data,
        format="json"
    )

    assert res.status_code == 403

    appointment_entries = AppointmentEntry.objects.all()
    assert len(appointment_entries) == 0


@pytest.mark.django_db
def test_get_single_appointment_entry(
    authenticated_user,
    add_appointment_entry
):
    """
    GIVEN a Django application
    WHEN the user requests to retrieve an appointment
    THEN check that the appointment is retrieved
    """
    current_date = date.today()

    client, user = authenticated_user

    appointment = add_appointment_entry(
        title="Dentist",
        date=current_date,
        time_from="09:00:00",
        time_until="10:00:00",
        user=user,
    )

    res = client.get(
        f"/api/appointments/{current_date}/{appointment.id}/",
        format="json"
    )

    assert res.status_code == 200
    assert res.data["user"] == user.id
    assert res.data["title"] == "Dentist"
    assert res.data["time_from"] == "09:00:00"
    assert res.data["time_until"] == "10:00:00"


@pytest.mark.django_db
@pytest.mark.parametrize("invalid_id", ["random", "1", 14258])
def test_get_single_appointment_entry_incorrect_id(authenticated_user, invalid_id):
    """
    GIVEN a Django application
    WHEN the user requests to retrieve an appointment with an incorrect id
    THEN check the appointment is not retrieved
    """
    (client, *_) = authenticated_user

    current_date = date.today()

    res = client.get(f"/api/appointments/{current_date}/{invalid_id}/")

    assert res.status_code == 404


@pytest.mark.django_db
@pytest.mark.parametrize("test_data", [
    {
        "requested_date": "2023-07-06",
        "expected_number_of_entries": 2
    },
    {
        "requested_date": "2023-07-04",
        "expected_number_of_entries": 1
    },
    {
        "requested_date": "2023-07-09",
        "expected_number_of_entries": 1
    }
])
def test_get_all_appointment_entries_by_date(
    authenticated_user,
    add_appointment_entry,
    test_data
):
    """
    GIVEN a Django application
    WHEN the user requests to retrieve all appointments by date
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

    res = client.get(f"/api/appointments/{test_data['requested_date']}/")

    assert res.status_code == 200
    assert res.data[0]["date"] == test_data['requested_date']

    appointment_entries = AppointmentEntry.objects.filter(
        date=test_data['requested_date'])
    assert len(appointment_entries) == test_data['expected_number_of_entries']


@pytest.mark.django_db
def test_remove_appointment_entry(
    authenticated_user,
    add_appointment_entry
):
    """
    GIVEN a Django application
    WHEN the user requests to remove an appointment
    THEN the appointment is removed
    """
    appointment_entries = AppointmentEntry.objects.all()
    assert len(appointment_entries) == 0

    current_date = date.today()

    client, user = authenticated_user

    appointment_entry = add_appointment_entry(
        title="Dentist",
        date=current_date,
        time_from="09:00:00",
        time_until="10:00:00",
        user=user,
    )

    res = client.get(
        f"/api/appointments/{current_date}/{appointment_entry.id}/", format="json")

    assert res.status_code == 200
    assert res.data["title"] == "Dentist"

    res_delete = client.delete(
        f"/api/appointments/{current_date}/{appointment_entry.id}/", format="json")

    assert res_delete.status_code == 204

    res_retrieve = client.get(
        f"/api/appointments/{current_date}/", format="json")

    assert res_retrieve.status_code == 200
    assert len(res_retrieve.data) == 0

    assert not AppointmentEntry.objects.filter(id=appointment_entry.id).exists()

    appointment_entries = AppointmentEntry.objects.all()
    assert len(appointment_entries) == 0


@pytest.mark.django_db
@pytest.mark.parametrize("test_data", [
    {
        "incorrect_id": "random",
        "expected_status_code": 404
    },
    {
        "incorrect_id": "1",
        "expected_status_code": 404
    },
    {
        "incorrect_id": 12756,
        "expected_status_code": 404
    },
])
def test_remove_appointment_invalid_id(
    authenticated_user,
    test_data
):
    """
    GIVEN a Django application
    WHEN the user requests to remove an appointment with an invalid id
    THEN the appointment is not removed
    """
    appointment_entries = AppointmentEntry.objects.all()
    assert len(appointment_entries) == 0

    current_date = date.today()

    (client, *_) = authenticated_user

    res = client.delete(
        f"/api/appointments/{current_date}/{test_data['incorrect_id']}/", format="json")

    assert res.status_code == test_data["expected_status_code"]

    updated_appointment_entries = AppointmentEntry.objects.all()
    assert len(appointment_entries) == len(updated_appointment_entries)
    assert len(updated_appointment_entries) == 0


@pytest.mark.django_db
@pytest.mark.parametrize("requested_date", [
    "2023-07-06", "2023-03-05", "2022-09-16"
])
def test_remove_appointment_not_current_date(
    authenticated_user, requested_date
):
    """
    GIVEN a Django application
    WHEN the user requests to remove an appointment when the date is not today
    THEN the appointment is not removed
    """
    appointment_entries = AppointmentEntry.objects.all()
    assert len(appointment_entries) == 0

    (client, *_) = authenticated_user

    res = client.delete(
        f"/api/appointments/{requested_date}/1/", format="json")

    assert res.status_code == 403

    updated_appointment_entries = AppointmentEntry.objects.all()
    assert len(appointment_entries) == len(updated_appointment_entries)
    assert len(updated_appointment_entries) == 0


@pytest.mark.django_db
@pytest.mark.parametrize("test_data", [
    {
        "payload": {
            "title": "Dentist",
            "date": "2023-07-06",
            "time_from": "10:00:00",
            "time_until": "11:00:00",
        }
    },
    {
        "payload": {
            "title": "Dentist",
            "date": "2023-07-06",
            "time_from": "10:00:00",
            "time_until": "11:00:00",
        }
    }
])
def test_update_appointment_entry(
    authenticated_user,
    add_appointment_entry,
    test_data
):
    """
    GIVEN a Django application
    WHEN the user requests to update an appointment
    THEN the appointment is updated
    """
    appointment_entries = AppointmentEntry.objects.all()
    assert len(appointment_entries) == 0

    current_date = date.today()

    client, user = authenticated_user

    appointment_entry = add_appointment_entry(
        title="Dentist",
        date="2023-07-06",
        time_from="09:00:00",
        time_until="10:00:00",
        user=user,
    )

    test_data["payload"]["user"] = user.id
    test_data["payload"]["date"] = current_date

    res = client.put(
        f"/api/appointments/{current_date}/{appointment_entry.id}/",
        test_data["payload"],
        format="json"
    )

    assert res.status_code == 200
    assert res.data["time_from"] == "10:00:00"
    assert res.data["time_until"] == "11:00:00"

    res_check = client.get(
        f"/api/appointments/{current_date}/{appointment_entry.id}/",
        format="json"
    )

    assert res_check.status_code == 200
    assert res.data["time_from"] == "10:00:00"
    assert res.data["time_until"] == "11:00:00"

    appointment_entries = AppointmentEntry.objects.all()
    assert len(appointment_entries) == 1


@pytest.mark.django_db
@pytest.mark.parametrize("test_data", [
    {
        "incorrect_id": "random",
        "expected_status_code": 404
    },
    {
        "incorrect_id": "1",
        "expected_status_code": 404
    },
    {
        "incorrect_id": 12574,
        "expected_status_code": 404
    }
])
def test_update_appointment_entry_incorrect_data(
    authenticated_user,
    test_data
):
    """
    GIVEN a Django application
    WHEN the user requests to update an appointment with an incorrect id
    THEN the appointment is not updated
    """
    (client, *_) = authenticated_user

    current_date = date.today()

    res = client.put(
        f"/api/appointments/{current_date}/{test_data['incorrect_id']}/",
        format="json"
    )

    assert res.status_code == test_data["expected_status_code"]


@pytest.mark.django_db
@pytest.mark.parametrize("requested_date", [
    "2023-07-06", "2023-03-05", "2022-09-16"
])
def test_update_appointment_entry_incorrect_data(
    authenticated_user,
    requested_date
):
    """
    GIVEN a Django application
    WHEN the user requests to update an appointment with an incorrect id
    THEN the appointment is not updated
    """
    (client, *_) = authenticated_user

    res = client.put(
        f"/api/appointments/{requested_date}/1/",
        format="json"
    )

    assert res.status_code == 403


@pytest.mark.django_db
@pytest.mark.parametrize("test_data", [
    {
        "payload": {},
        "expected_status_code": 400
    },
    {
        "payload": {
            "title": "Dentist",
            "date": "2023-07-06",
            "time from": "09:00:00",
            "time until": "10:00:00",
        },
        "expected_status_code": 400
    }
])
def test_update_appointment_entry_invalid_json(
    authenticated_user,
    add_appointment_entry,
    test_data
):
    """
    GIVEN a Django application
    WHEN the user requests to update an appointment with invalid JSON
    THEN the appointment is not updated
    """
    client, user = authenticated_user

    current_date = date.today()

    appointment_entry = add_appointment_entry(
        title="Dentist",
        date="2023-07-06",
        time_from="09:00:00",
        time_until="10:00:00",
        user=user,
    )

    res = client.put(
        f"/api/appointments/{current_date}/{appointment_entry.id}/",
        test_data["payload"],
        format="json"
    )

    assert res.status_code == test_data["expected_status_code"]
