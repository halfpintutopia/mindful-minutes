from datetime import date
# https://dennisokeeffe.medium.com/mocking-python-datetime-in-tests-with-freezegun-f5532307d6d6
from freezegun import freeze_time

import pytest

from journal.models import ImprovementEntry


@pytest.mark.django_db
def test_add_improvement_entry(authenticated_user):
    """
    GIVEN a Django application
    WHEN the user requests to add an improvement entry
    THEN check that the improvement entry is added
    """
    improvement_entries = ImprovementEntry.objects.all()
    assert len(improvement_entries) == 0

    current_date = date.today()

    client, user = authenticated_user

    improvement_data = {
        "content": "I need to listen more and talk less.",
        "user": user.id,
    }

    res = client.post(
        f"/api/improvement/{current_date}/",
        improvement_data,
        format="json"
    )

    print("Response data", res.data)

    assert res.status_code == 201
    assert res.data["user"] == user.id
    assert res.data["content"] == "I need to listen more and talk less."

    improvement_entries = ImprovementEntry.objects.all()
    assert len(improvement_entries) == 1


@pytest.mark.django_db
@pytest.mark.parametrize("test_data", [
    {
        "payload": {},
        "status_code": 400
    },
    {
        "payload": {
            "content entry": "I need to listen more and talk less.",
        },
        "status_code": 400
    }
])
def test_add_improvement_entry_incorrect_json(authenticated_user, test_data):
    """
    GIVEN a Django application
    WHEN the user requests to add an improvement entry with an invalid payload
    THEN the payload is not sent
    """
    improvement_entries = ImprovementEntry.objects.all()
    assert len(improvement_entries) == 0

    current_date = date.today()

    client, user = authenticated_user

    test_data["payload"]["user"] = user.id

    res = client.post(
        f"/api/improvement/{current_date}/",
        test_data["payload"],
        format="json"
    )
    assert res.status_code == 400

    improvement_entries = ImprovementEntry.objects.all()
    assert len(improvement_entries) == 0


@pytest.mark.django_db
@pytest.mark.parametrize("date_param", ["2023-07-01", "2023-06-20"])
def test_add_improvement_entry_not_current_date(
    authenticated_user,
    date_param
):
    """
    GIVEN a Django application
    WHEN the user attempts to add an improvement entry on a date,
    that is not the current date
    THEN the improvement entry is not created
    """
    improvement_entries = ImprovementEntry.objects.all()
    assert len(improvement_entries) == 0

    client, user = authenticated_user

    improvement_data = {
        "content": "I need to listen more and talk less.",
        "user": user.id,
    }

    res = client.post(
        f"/api/improvement/{date_param}/",
        improvement_data,
        format="json"
    )

    assert res.status_code == 403

    improvement_entries = ImprovementEntry.objects.all()
    assert len(improvement_entries) == 0


@pytest.mark.django_db
def test_get_single_improvement_entry(
    authenticated_user,
    add_improvement_entry
):
    """
    GIVEN a Django application
    WHEN the user requests to retrieve an improvement entry
    THEN check that the improvement entry is retrieved
    """
    current_date = date.today()

    client, user = authenticated_user

    improvement = add_improvement_entry(
        content="I need to listen more and talk less.",
        user=user,
    )

    res = client.get(
        f"/api/improvement/{current_date}/{improvement.id}/",
        format="json"
    )

    assert res.status_code == 200
    assert res.data["user"] == user.id
    assert res.data["content"] == "I need to listen more and talk less."


@pytest.mark.django_db
@pytest.mark.parametrize("invalid_id", ["random", "1", 14258])
def test_get_single_improvement_entry_incorrect_id(
    authenticated_user,
    invalid_id
):
    """
    GIVEN a Django application
    WHEN the user requests to retrieve an improvement entry with an incorrect id
    THEN check the improvement entry is not retrieved
    """
    (client, *_) = authenticated_user

    current_date = date.today()

    res = client.get(f"/api/improvement/{current_date}/{invalid_id}/")

    assert res.status_code == 404


@pytest.mark.django_db
def test_get_all_improvement_entries_by_current_date(
    authenticated_user,
    add_improvement_entry
):
    """
    GIVEN a Django application
    WHEN the user requests to retrieve all improvement entries
    by current date
    THEN check all improvement entries are retrieved
    """
    improvement_entries = ImprovementEntry.objects.all()
    assert len(improvement_entries) == 0

    current_date = date.today()

    client, user = authenticated_user

    add_improvement_entry(
        content="I need to listen more and talk less.",
        user=user,
    )

    res = client.get(f"/api/improvement/{str(current_date)}/")

    assert res.status_code == 200
    assert res.data[0]["created_on"] == str(current_date)

    improvement_entries = ImprovementEntry.objects.filter(
        created_on__date=current_date)
    assert len(improvement_entries) == 1


@pytest.mark.django_db
@pytest.mark.parametrize("created_on_timestamp", [
    "2023-04-06 12:00:00",
    "2023-06-04 10:30:00",
    "2022-07-09 19:45:00",
])
def test_get_all_improvement_entries_by_date(
    authenticated_user,
    add_improvement_entry,
    created_on_timestamp
):
    """
    GIVEN a Django application
    WHEN the user requests to retrieve all improvement entries by date
    THEN check all improvement entries are retrieved
    """
    with freeze_time(created_on_timestamp):
        improvement_entries = ImprovementEntry.objects.all()
        assert len(improvement_entries) == 0

        current_date = date.today()

        client, user = authenticated_user

        add_improvement_entry(
            content="I need to listen more and talk less.",
            user=user,
        )

        res = client.get(f"/api/improvement/{str(current_date)}/")

        assert res.status_code == 200
        assert res.data[0]["created_on"] == str(current_date)

        improvement_entries = ImprovementEntry.objects.filter(
            created_on__date=current_date)
        assert len(improvement_entries) == 1


@pytest.mark.django_db
def test_remove_improvement_entry(
    authenticated_user,
    add_improvement_entry
):
    """
    GIVEN a Django application
    WHEN the user requests to remove an improvement entry
    THEN the improvement entry is removed
    """
    improvement_entries = ImprovementEntry.objects.all()
    assert len(improvement_entries) == 0

    current_date = date.today()

    client, user = authenticated_user

    improvement_entry = add_improvement_entry(
        content="I need to listen more and talk less.",
        user=user,
    )

    res = client.get(
        f"/api/improvement/{current_date}/{improvement_entry.id}/",
        format="json"
    )

    assert res.status_code == 200
    assert res.data["content"] == "I need to listen more and talk less."

    res_delete = client.delete(
        f"/api/improvement/{current_date}/{improvement_entry.id}/",
        format="json"
    )

    assert res_delete.status_code == 204

    res_retrieve = client.get(
        f"/api/improvement/{current_date}/", format="json")

    assert res_retrieve.status_code == 200
    assert len(res_retrieve.data) == 0

    assert not ImprovementEntry.objects.filter(id=improvement_entry.id).exists()

    improvement_entries = ImprovementEntry.objects.all()
    assert len(improvement_entries) == 0


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
def test_remove_improvement_invalid_id(
    authenticated_user,
    test_data
):
    """
    GIVEN a Django application
    WHEN the user requests to remove an improvement entry with an invalid id
    THEN the improvement entry is not removed
    """
    improvement_entries = ImprovementEntry.objects.all()
    assert len(improvement_entries) == 0

    current_date = date.today()

    (client, *_) = authenticated_user

    res = client.delete(
        f"/api/improvement/{current_date}/{test_data['incorrect_id']}/",
        format="json"
    )

    assert res.status_code == test_data["expected_status_code"]

    updated_improvement_entries = ImprovementEntry.objects.all()
    assert len(improvement_entries) == len(updated_improvement_entries)
    assert len(updated_improvement_entries) == 0


@pytest.mark.django_db
@pytest.mark.parametrize("requested_date", [
    "2024-07-06", "2023-03-05", "2022-09-16"
])
def test_remove_improvement_not_current_date(
    authenticated_user, requested_date
):
    """
    GIVEN a Django application
    WHEN the user requests to remove an improvement entry when the date is not today
    THEN the improvement entry is not removed
    """
    improvement_entries = ImprovementEntry.objects.all()
    assert len(improvement_entries) == 0

    (client, *_) = authenticated_user

    res = client.delete(
        f"/api/improvement/{requested_date}/1/", format="json")

    assert res.status_code == 403

    updated_improvement_entries = ImprovementEntry.objects.all()
    assert len(improvement_entries) == len(updated_improvement_entries)
    assert len(updated_improvement_entries) == 0


@pytest.mark.django_db
@pytest.mark.parametrize("test_data", [
    {
        "payload": {
            "content": "I need to listen more and talk less. Focus on mantras during meditation.",
        }
    },
    {
        "payload": {
            "content": "I need to be less distracted while meditating.",
        }
    }
])
def test_update_improvement_entry(
    authenticated_user,
    add_improvement_entry,
    test_data
):
    """
    GIVEN a Django application
    WHEN the user requests to update an improvement entry
    THEN the improvement entry is updated
    """
    improvement_entries = ImprovementEntry.objects.all()
    assert len(improvement_entries) == 0

    current_date = date.today()

    client, user = authenticated_user

    improvement_entry = add_improvement_entry(
        content="I need to listen more and talk less.",
        user=user,
    )

    test_data["payload"]["user"] = user.id

    res = client.put(
        f"/api/improvement/{current_date}/{improvement_entry.id}/",
        test_data["payload"],
        format="json"
    )

    assert res.status_code == 200
    assert res.data["content"] == test_data["payload"]["content"]

    res_check = client.get(
        f"/api/improvement/{current_date}/{improvement_entry.id}/",
        format="json"
    )

    assert res_check.status_code == 200
    assert res.data["content"] == test_data["payload"]["content"]

    improvement_entries = ImprovementEntry.objects.all()
    assert len(improvement_entries) == 1


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
def test_update_improvement_entry_incorrect_data(
    authenticated_user,
    add_improvement_entry,
    test_data
):
    """
    GIVEN a Django application
    WHEN the user requests to update an improvement entry with an incorrect id
    THEN the improvement entry is not updated
    """
    client, user = authenticated_user

    current_date = date.today()

    add_improvement_entry(
        content="I need to listen more and talk less.",
        user=user,
    )

    improvement_data = {
        "content": "I need to be less distracted while meditating.",
        "user": user.id,
    }

    res = client.put(
        f"/api/improvement/{current_date}/{test_data['incorrect_id']}/",
        improvement_data,
        format="json"
    )

    print("response data", res)

    assert res.status_code == test_data["expected_status_code"]


@pytest.mark.django_db
@pytest.mark.parametrize("requested_date", [
    "2024-07-06", "2023-03-05", "2022-09-16"
])
def test_update_improvement_entry_incorrect_date(
    authenticated_user,
    requested_date
):
    """
    GIVEN a Django application
    WHEN the user requests to update an improvement entry with an incorrect date
    THEN the improvement entry is not and permission denied
    """
    (client, *_) = authenticated_user

    res = client.put(
        f"/api/improvement/{requested_date}/1/",
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
            "content entry": "I need to listen more and talk less.",
        },
        "expected_status_code": 400
    }
])
def test_update_improvement_entry_invalid_json(
    authenticated_user,
    add_improvement_entry,
    test_data
):
    """
    GIVEN a Django application
    WHEN the user requests to update an improvement entry with invalid JSON
    THEN the improvement entry is not updated
    """
    client, user = authenticated_user

    current_date = date.today()

    improvement_entry = add_improvement_entry(
        content="Dentist",
        user=user,
    )

    res = client.put(
        f"/api/improvement/{current_date}/{improvement_entry.id}/",
        test_data["payload"],
        format="json"
    )

    assert res.status_code == test_data["expected_status_code"]
