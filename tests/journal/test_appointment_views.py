from datetime import date
# https://dennisokeeffe.medium.com/mocking-python-datetime-in-tests-with-freezegun-f5532307d6d6
from freezegun import freeze_time

import pytest

from journal.models import AppointmentEntry


@pytest.mark.django_db
def test_add_appointment_entry(authenticated_user):
    """
    GIVEN a Django application
    WHEN the user requests to add an appointment entry
    THEN check that the appointment entry is added
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
        f"/api/appointments/{str(current_date)}/",
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
    WHEN the user requests to add an appointment entry with an invalid payload
    THEN the payload is not sent
    """
    appointment_entries = AppointmentEntry.objects.all()
    assert len(appointment_entries) == 0

    current_date = date.today()

    client, user = authenticated_user

    test_data["payload"]["date"] = current_date
    test_data["payload"]["user"] = user.id

    res = client.post(
        f"/api/appointments/{str(current_date)}/",
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
    WHEN the user requests to retrieve an appointment entry
    THEN check that the appointment entry is retrieved
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
def test_get_single_appointment_entry_incorrect_id(
    authenticated_user,
    invalid_id
):
    """
    GIVEN a Django application
    WHEN the user requests to retrieve an appointment entry with an incorrect id
    THEN check the appointment entry is not retrieved
    """
    (client, *_) = authenticated_user

    current_date = date.today()

    res = client.get(f"/api/appointments/{current_date}/{invalid_id}/")

    assert res.status_code == 404


@pytest.mark.django_db
def test_get_all_appointment_entries_by_current_date(
    authenticated_user,
    add_appointment_entry,
):
    """
    GIVEN a Django application
    WHEN the user requests to retrieve all appointment entries
    by current date
    THEN check all appointment entries are retrieved
    """
    appointment_entries = AppointmentEntry.objects.all()
    assert len(appointment_entries) == 0

    current_date = date.today()

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

    res = client.get(f"/api/appointments/{str(current_date)}/")

    assert res.status_code == 200
    assert res.data[0]["created_on"] == str(current_date)

    appointment_entries = AppointmentEntry.objects.filter(
        created_on__date=current_date)
    assert len(appointment_entries) == 4


@pytest.mark.django_db
@pytest.mark.parametrize("created_on_timestamp", [
    "2023-07-06 12:00:00",
    "2023-06-04 10:30:00",
    "2022-07-09 19:45:00",
])
def test_get_all_appointment_entries_by_date(
    authenticated_user,
    add_appointment_entry,
    created_on_timestamp
):
    """
    GIVEN a Django application
    WHEN the user requests to retrieve all appointment entries by date
    THEN check all appointment entries are retrieved
    """
    with freeze_time(created_on_timestamp):
        appointment_entries = AppointmentEntry.objects.all()
        assert len(appointment_entries) == 0

        current_date = date.today()

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

        res = client.get(f"/api/appointments/{str(current_date)}/")

        assert res.status_code == 200
        assert res.data[0]["created_on"] == str(current_date)

        appointment_entries = AppointmentEntry.objects.filter(
            created_on__date=current_date)
        assert len(appointment_entries) == 4


@pytest.mark.django_db
def test_remove_appointment_entry(
    authenticated_user,
    add_appointment_entry
):
    """
    GIVEN a Django application
    WHEN the user requests to remove an appointment entry
    THEN the appointment entry is removed
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
        f"/api/appointments/{current_date}/{appointment_entry.id}/",
        format="json"
    )

    assert res.status_code == 200
    assert res.data["title"] == "Dentist"

    res_delete = client.delete(
        f"/api/appointments/{current_date}/{appointment_entry.id}/",
        format="json"
    )

    assert res_delete.status_code == 204

    res_retrieve = client.get(
        f"/api/appointments/{str(current_date)}/", format="json")

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
    WHEN the user requests to remove an appointment entry with an invalid id
    THEN the appointment entry is not removed
    """
    appointment_entries = AppointmentEntry.objects.all()
    assert len(appointment_entries) == 0

    current_date = date.today()

    (client, *_) = authenticated_user

    res = client.delete(
        f"/api/appointments/{current_date}/{test_data['incorrect_id']}/",
        format="json"
    )

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
    WHEN the user requests to remove an appointment entry when the date is not today
    THEN the appointment entry is not removed
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
    WHEN the user requests to update an appointment entry
    THEN the appointment entry is updated
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
    WHEN the user requests to update an appointment entry with an incorrect id
    THEN the appointment entry is not updated
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
def test_update_appointment_entry_incorrect_date(
    authenticated_user,
    requested_date
):
    """
    GIVEN a Django application
    WHEN the user requests to update an appointment entry with an incorrect date
    THEN the appointment entry is not and permission denied
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
    WHEN the user requests to update an appointment entry with invalid JSON
    THEN the appointment entry is not updated
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
