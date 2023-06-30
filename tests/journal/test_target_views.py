from datetime import date
# https://dennisokeeffe.medium.com/mocking-python-datetime-in-tests-with-freezegun-f5532307d6d6
from freezegun import freeze_time

import pytest

from journal.models import TargetEntry


@pytest.mark.django_db
def test_add_target_entry(authenticated_user):
    """
    GIVEN a Django application
    WHEN the user requests to add an target entry
    THEN check that the target entry is added
    """
    target_entries = TargetEntry.objects.all()
    assert len(target_entries) == 0

    current_date = date.today()

    client, user = authenticated_user

    target_data = {
        "title": "2 minute cold shower",
        "order": 1,
        "user": user.id,
    }

    res = client.post(
        f"/api/targets/{current_date}/",
        target_data,
        format="json"
    )

    assert res.status_code == 201
    assert res.data["user"] == user.id
    assert res.data["title"] == "2 minute cold shower"
    assert res.data["order"] == 1

    target_entries = TargetEntry.objects.all()
    assert len(target_entries) == 1


@pytest.mark.django_db
@pytest.mark.parametrize("test_data", [
    {
        "payload": {},
        "status_code": 400
    },
    {
        "payload": {
            "title": "2 minute cold shower",
            "content entry": "09:00:00",
            "order": 1
        },
        "status_code": 400
    }
])
def test_add_target_entry_incorrect_json(authenticated_user, test_data):
    """
    GIVEN a Django application
    WHEN the user requests to add an target entry with an invalid payload
    THEN the payload is not sent
    """
    target_entries = TargetEntry.objects.all()
    assert len(target_entries) == 0

    current_date = date.today()

    client, user = authenticated_user

    test_data["payload"]["user"] = user.id

    res = client.post(
        f"/api/targets/{current_date}/",
        {},
        format="json"
    )
    assert res.status_code == 400

    target_entries = TargetEntry.objects.all()
    assert len(target_entries) == 0


@pytest.mark.django_db
@pytest.mark.parametrize("date_param", ["2023-07-01", "2023-06-20"])
def test_add_target_entry_not_current_date(
    authenticated_user,
    date_param
):
    """
    GIVEN a Django application
    WHEN the user attempts to add an target entry on a date,
    that is not the current date
    THEN the target entry is not created
    """
    target_entries = TargetEntry.objects.all()
    assert len(target_entries) == 0

    current_date = date.today()

    client, user = authenticated_user

    target_data = {
        "title": "2 minute cold shower",
        "order": 1,
        "user": user.id,
    }

    res = client.post(
        f"/api/targets/{date_param}/",
        target_data,
        format="json"
    )

    assert res.status_code == 403

    target_entries = TargetEntry.objects.all()
    assert len(target_entries) == 0


@pytest.mark.django_db
def test_get_single_target_entry(
    authenticated_user,
    add_target_entry
):
    """
    GIVEN a Django application
    WHEN the user requests to retrieve an target entry
    THEN check that the target entry is retrieved
    """
    current_date = date.today()

    client, user = authenticated_user

    target = add_target_entry(
        title="2 minute cold shower",
        order=1,
        user=user,
    )

    res = client.get(
        f"/api/targets/{current_date}/{target.id}/",
        format="json"
    )

    assert res.status_code == 200
    assert res.data["user"] == user.id
    assert res.data["title"] == "2 minute cold shower"
    assert res.data["order"] == 1


@pytest.mark.django_db
@pytest.mark.parametrize("invalid_id", ["random", "1", 14258])
def test_get_single_target_entry_incorrect_id(
    authenticated_user,
    invalid_id
):
    """
    GIVEN a Django application
    WHEN the user requests to retrieve an target entry with an incorrect id
    THEN check the target entry is not retrieved
    """
    (client, *_) = authenticated_user

    current_date = date.today()

    res = client.get(f"/api/targets/{current_date}/{invalid_id}/")

    assert res.status_code == 404


@pytest.mark.django_db
def test_get_all_target_entries_by_current_date(
    authenticated_user,
    add_target_entry
):
    """
    GIVEN a Django application
    WHEN the user requests to retrieve all target entries
    by current date
    THEN check all target entries are retrieved
    """
    target_entries = TargetEntry.objects.all()
    assert len(target_entries) == 0

    current_date = date.today()

    client, user = authenticated_user

    add_target_entry(
        title="2 minute cold shower",
        order=1,
        user=user,
    )

    add_target_entry(
        title="20 minute meditation",
        order=2,
        user=user,
    )

    add_target_entry(
        title="Meet Andy for lunch",
        order=3,
        user=user,
    )

    add_target_entry(
        title="Read 30 pages of Momo in German",
        order=4,
        user=user,
    )

    res = client.get(f"/api/targets/{str(current_date)}/")

    assert res.status_code == 200
    assert res.data[0]["created_on"] == str(current_date)

    target_entries = TargetEntry.objects.filter(
        created_on__date=current_date)
    assert len(target_entries) == 4


@pytest.mark.django_db
@pytest.mark.parametrize("created_on_timestamp", [
    "2023-07-06 12:00:00",
    "2023-06-04 10:30:00",
    "2022-07-09 19:45:00",
])
def test_get_all_target_entries_by_date(
    authenticated_user,
    add_target_entry,
    created_on_timestamp
):
    """
    GIVEN a Django application
    WHEN the user requests to retrieve all target entries by date
    THEN check all target entries are retrieved
    """
    with freeze_time(created_on_timestamp):
        target_entries = TargetEntry.objects.all()
        assert len(target_entries) == 0

        current_date = date.today()

        client, user = authenticated_user

        add_target_entry(
            title="2 minute cold shower",
            order=1,
            user=user,
        )

        add_target_entry(
            title="20 minute meditation",
            order=2,
            user=user,
        )

        add_target_entry(
            title="Meet Andy for lunch",
            order=3,
            user=user,
        )

        add_target_entry(
            title="Read 30 pages of Momo in German",
            order=4,
            user=user,
        )

        res = client.get(f"/api/targets/{str(current_date)}/")

        assert res.status_code == 200
        assert res.data[0]["created_on"] == str(current_date)

        target_entries = TargetEntry.objects.filter(
            created_on__date=current_date)
        assert len(target_entries) == 4


@pytest.mark.django_db
def test_remove_target_entry(
    authenticated_user,
    add_target_entry
):
    """
    GIVEN a Django application
    WHEN the user requests to remove an target entry
    THEN the target entry is removed
    """
    target_entries = TargetEntry.objects.all()
    assert len(target_entries) == 0

    current_date = date.today()

    client, user = authenticated_user

    target_entry = add_target_entry(
        title="2 minute cold shower",
        order=1,
        user=user,
    )

    res = client.get(
        f"/api/targets/{current_date}/{target_entry.id}/",
        format="json"
    )

    assert res.status_code == 200
    assert res.data["title"] == "2 minute cold shower"
    assert res.data["order"] == 1

    res_delete = client.delete(
        f"/api/targets/{current_date}/{target_entry.id}/",
        format="json"
    )

    assert res_delete.status_code == 204

    res_retrieve = client.get(
        f"/api/targets/{current_date}/", format="json")

    assert res_retrieve.status_code == 200
    assert len(res_retrieve.data) == 0

    assert not TargetEntry.objects.filter(id=target_entry.id).exists()

    target_entries = TargetEntry.objects.all()
    assert len(target_entries) == 0


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
def test_remove_target_invalid_id(
    authenticated_user,
    test_data
):
    """
    GIVEN a Django application
    WHEN the user requests to remove an target entry with an invalid id
    THEN the target entry is not removed
    """
    target_entries = TargetEntry.objects.all()
    assert len(target_entries) == 0

    current_date = date.today()

    (client, *_) = authenticated_user

    res = client.delete(
        f"/api/targets/{current_date}/{test_data['incorrect_id']}/",
        format="json"
    )

    assert res.status_code == test_data["expected_status_code"]

    updated_target_entries = TargetEntry.objects.all()
    assert len(target_entries) == len(updated_target_entries)
    assert len(updated_target_entries) == 0


@pytest.mark.django_db
@pytest.mark.parametrize("requested_date", [
    "2023-07-06", "2023-03-05", "2022-09-16"
])
def test_remove_target_not_current_date(
    authenticated_user, requested_date
):
    """
    GIVEN a Django application
    WHEN the user requests to remove an target entry when the date is not today
    THEN the target entry is not removed
    """
    target_entries = TargetEntry.objects.all()
    assert len(target_entries) == 0

    (client, *_) = authenticated_user

    res = client.delete(
        f"/api/targets/{requested_date}/1/", format="json")

    assert res.status_code == 403

    updated_target_entries = TargetEntry.objects.all()
    assert len(target_entries) == len(updated_target_entries)
    assert len(updated_target_entries) == 0


@pytest.mark.django_db
@pytest.mark.parametrize("test_data", [
    {
        "payload": {
            "title": "20 minutes meditation",
            "order": 1,
        }
    },
    {
        "payload": {
            "title": "2 minute cold shower",
            "order": 2,
        }
    },
    {
        "payload": {
            "title": "20 minutes meditation",
            "order": 2,
        }
    }
])
def test_update_target_entry(
    authenticated_user,
    add_target_entry,
    test_data
):
    """
    GIVEN a Django application
    WHEN the user requests to update an target entry
    THEN the target entry is updated
    """
    target_entries = TargetEntry.objects.all()
    assert len(target_entries) == 0

    current_date = date.today()

    client, user = authenticated_user

    target_entry = add_target_entry(
        title="2 minute cold shower",
        order=1,
        user=user,
    )

    test_data["payload"]["user"] = user.id

    res = client.put(
        f"/api/targets/{current_date}/{target_entry.id}/",
        test_data["payload"],
        format="json"
    )

    assert res.status_code == 200
    assert res.data["title"] == test_data["payload"]["title"]
    assert res.data["order"] == test_data["payload"]["order"]

    res_check = client.get(
        f"/api/targets/{current_date}/{target_entry.id}/",
        format="json"
    )

    assert res_check.status_code == 200
    assert res.data["title"] == test_data["payload"]["title"]
    assert res.data["order"] == test_data["payload"]["order"]

    target_entries = TargetEntry.objects.all()
    assert len(target_entries) == 1


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
def test_update_target_entry_incorrect_data(
    authenticated_user,
    add_target_entry,
    test_data
):
    """
    GIVEN a Django application
    WHEN the user requests to update an target entry with an incorrect id
    THEN the target entry is not updated
    """
    client, user = authenticated_user

    current_date = date.today()

    add_target_entry(
        title="2 minute cold shower",
        order=1,
        user=user,
    )

    target_data = {
        "title": "2 minute cold shower",
        "order": 1,
        "user": user.id,
    }

    res = client.put(
        f"/api/targets/{current_date}/{test_data['incorrect_id']}/",
        target_data,
        format="json"
    )

    print("response data", res)

    assert res.status_code == test_data["expected_status_code"]


@pytest.mark.django_db
@pytest.mark.parametrize("requested_date", [
    "2023-07-06", "2023-03-05", "2022-09-16"
])
def test_update_target_entry_incorrect_date(
    authenticated_user,
    requested_date
):
    """
    GIVEN a Django application
    WHEN the user requests to update an target entry with an incorrect date
    THEN the target entry is not and permission denied
    """
    (client, *_) = authenticated_user

    res = client.put(
        f"/api/targets/{requested_date}/1/",
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
            "title input": "2 minute cold shower",
            "order": 1,
        },
        "expected_status_code": 400
    }
])
def test_update_target_entry_invalid_json(
    authenticated_user,
    add_target_entry,
    test_data
):
    """
    GIVEN a Django application
    WHEN the user requests to update an target entry with invalid JSON
    THEN the target entry is not updated
    """
    client, user = authenticated_user

    current_date = date.today()

    target_entry = add_target_entry(
        title="Dentist",
        order=1,
        user=user,
    )

    res = client.put(
        f"/api/targets/{current_date}/{target_entry.id}/",
        test_data["payload"],
        format="json"
    )

    assert res.status_code == test_data["expected_status_code"]
