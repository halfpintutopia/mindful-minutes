from datetime import date
# https://dennisokeeffe.medium.com/mocking-python-datetime-in-tests-with-freezegun-f5532307d6d6
from freezegun import freeze_time

import pytest

from journal.models import WinEntry


@pytest.mark.django_db
def test_add_win_entry(authenticated_user):
    """
    GIVEN a Django application
    WHEN the user requests to add an win entry
    THEN check that the win entry is added
    """
    win_entries = WinEntry.objects.all()
    assert len(win_entries) == 0

    current_date = date.today()

    client, user = authenticated_user

    win_data = {
        "title": "Finished HTML and CSS",
        "user": user.id,
    }

    res = client.post(
        f"/api/wins/{current_date}/",
        win_data,
        format="json"
    )

    assert res.status_code == 201
    assert res.data["user"] == user.id
    assert res.data["title"] == "Finished HTML and CSS"

    win_entries = WinEntry.objects.all()
    assert len(win_entries) == 1


@pytest.mark.django_db
@pytest.mark.parametrize("test_data", [
    {
        "payload": {},
        "status_code": 400
    },
    {
        "payload": {
            "title entry": "Finished HTML and CSS",
        },
        "status_code": 400
    }
])
def test_add_win_entry_incorrect_json(authenticated_user, test_data):
    """
    GIVEN a Django application
    WHEN the user requests to add an win entry with an invalid payload
    THEN the payload is not sent
    """
    win_entries = WinEntry.objects.all()
    assert len(win_entries) == 0

    current_date = date.today()

    client, user = authenticated_user

    test_data["payload"]["user"] = user.id

    res = client.post(
        f"/api/wins/{current_date}/",
        {},
        format="json"
    )
    assert res.status_code == 400

    win_entries = WinEntry.objects.all()
    assert len(win_entries) == 0


@pytest.mark.django_db
@pytest.mark.parametrize("date_param", ["2023-07-01", "2023-06-20"])
def test_add_win_entry_not_current_date(
    authenticated_user,
    date_param
):
    """
    GIVEN a Django application
    WHEN the user attempts to add an win entry on a date,
    that is not the current date
    THEN the win entry is not created
    """
    win_entries = WinEntry.objects.all()
    assert len(win_entries) == 0

    client, user = authenticated_user

    win_data = {
        "title": "Finished HTML and CSS",
        "user": user.id,
    }

    res = client.post(
        f"/api/wins/{date_param}/",
        win_data,
        format="json"
    )

    assert res.status_code == 403

    win_entries = WinEntry.objects.all()
    assert len(win_entries) == 0


@pytest.mark.django_db
def test_get_single_win_entry(
    authenticated_user,
    add_win_entry
):
    """
    GIVEN a Django application
    WHEN the user requests to retrieve an win entry
    THEN check that the win entry is retrieved
    """
    current_date = date.today()

    client, user = authenticated_user

    win = add_win_entry(
        title="Finished HTML and CSS",
        user=user,
    )

    res = client.get(
        f"/api/wins/{current_date}/{win.id}/",
        format="json"
    )

    assert res.status_code == 200
    assert res.data["user"] == user.id
    assert res.data["title"] == "Finished HTML and CSS"


@pytest.mark.django_db
@pytest.mark.parametrize("invalid_id", ["random", "1", 14258])
def test_get_single_win_entry_incorrect_id(
    authenticated_user,
    invalid_id
):
    """
    GIVEN a Django application
    WHEN the user requests to retrieve an win entry with an incorrect id
    THEN check the win entry is not retrieved
    """
    (client, *_) = authenticated_user

    current_date = date.today()

    res = client.get(f"/api/wins/{current_date}/{invalid_id}/")

    assert res.status_code == 404


@pytest.mark.django_db
def test_get_all_win_entries_by_current_date(
    authenticated_user,
    add_win_entry
):
    """
    GIVEN a Django application
    WHEN the user requests to retrieve all win entries
    by current date
    THEN check all win entries are retrieved
    """
    win_entries = WinEntry.objects.all()
    assert len(win_entries) == 0

    current_date = date.today()

    client, user = authenticated_user

    add_win_entry(
        title="Finished HTML and CSS",
        user=user,
    )

    add_win_entry(
        title="Had a conversation in German",
        user=user,
    )

    add_win_entry(
        title="Hiked for 20 kms",
        user=user,
    )

    add_win_entry(
        title="Read 30 pages of Momo in German",
        user=user,
    )

    res = client.get(f"/api/wins/{str(current_date)}/")

    assert res.status_code == 200
    assert res.data[0]["created_on"] == str(current_date)

    win_entries = WinEntry.objects.filter(
        created_on__date=current_date)
    assert len(win_entries) == 4


@pytest.mark.django_db
@pytest.mark.parametrize("created_on_timestamp", [
    "2023-04-06 12:00:00",
    "2023-06-04 10:30:00",
    "2022-07-09 19:45:00",
])
def test_get_all_win_entries_by_date(
    authenticated_user,
    add_win_entry,
    created_on_timestamp
):
    """
    GIVEN a Django application
    WHEN the user requests to retrieve all win entries by date
    THEN check all win entries are retrieved
    """
    with freeze_time(created_on_timestamp):
        win_entries = WinEntry.objects.all()
        assert len(win_entries) == 0

        current_date = date.today()

        client, user = authenticated_user

        add_win_entry(
            title="Finished HTML and CSS",
            user=user,
        )

        add_win_entry(
            title="Had a conversation in German",
            user=user,
        )

        add_win_entry(
            title="Hiked for 20 kms",
            user=user,
        )

        add_win_entry(
            title="Read 30 pages of Momo in German",
            user=user,
        )

        res = client.get(f"/api/wins/{str(current_date)}/")

        assert res.status_code == 200
        assert res.data[0]["created_on"] == str(current_date)

        win_entries = WinEntry.objects.filter(
            created_on__date=current_date)
        assert len(win_entries) == 4


@pytest.mark.django_db
def test_remove_win_entry(
    authenticated_user,
    add_win_entry
):
    """
    GIVEN a Django application
    WHEN the user requests to remove an win entry
    THEN the win entry is removed
    """
    win_entries = WinEntry.objects.all()
    assert len(win_entries) == 0

    current_date = date.today()

    client, user = authenticated_user

    win_entry = add_win_entry(
        title="Finished HTML and CSS",
        user=user,
    )

    res = client.get(
        f"/api/wins/{current_date}/{win_entry.id}/",
        format="json"
    )

    assert res.status_code == 200
    assert res.data["title"] == "Finished HTML and CSS"

    res_delete = client.delete(
        f"/api/wins/{current_date}/{win_entry.id}/",
        format="json"
    )

    assert res_delete.status_code == 204

    res_retrieve = client.get(
        f"/api/wins/{current_date}/", format="json")

    assert res_retrieve.status_code == 200
    assert len(res_retrieve.data) == 0

    assert not WinEntry.objects.filter(id=win_entry.id).exists()

    win_entries = WinEntry.objects.all()
    assert len(win_entries) == 0


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
def test_remove_win_invalid_id(
    authenticated_user,
    test_data
):
    """
    GIVEN a Django application
    WHEN the user requests to remove an win entry with an invalid id
    THEN the win entry is not removed
    """
    win_entries = WinEntry.objects.all()
    assert len(win_entries) == 0

    current_date = date.today()

    (client, *_) = authenticated_user

    res = client.delete(
        f"/api/wins/{current_date}/{test_data['incorrect_id']}/",
        format="json"
    )

    assert res.status_code == test_data["expected_status_code"]

    updated_win_entries = WinEntry.objects.all()
    assert len(win_entries) == len(updated_win_entries)
    assert len(updated_win_entries) == 0


@pytest.mark.django_db
@pytest.mark.parametrize("requested_date", [
    "2024-07-06", "2023-03-05", "2022-09-16"
])
def test_remove_win_not_current_date(
    authenticated_user, requested_date
):
    """
    GIVEN a Django application
    WHEN the user requests to remove an win entry when the date is not today
    THEN the win entry is not removed
    """
    win_entries = WinEntry.objects.all()
    assert len(win_entries) == 0

    (client, *_) = authenticated_user

    res = client.delete(
        f"/api/wins/{requested_date}/1/", format="json")

    assert res.status_code == 403

    updated_win_entries = WinEntry.objects.all()
    assert len(win_entries) == len(updated_win_entries)
    assert len(updated_win_entries) == 0


@pytest.mark.django_db
@pytest.mark.parametrize("test_data", [
    {
        "payload": {
            "title": "Finished HTML and CSS",
        }
    },
    {
        "payload": {
            "title": "Had a conversation in German",
        }
    },
    {
        "payload": {
            "title": "Hiked for 20 kms",
        }
    }
])
def test_update_win_entry(
    authenticated_user,
    add_win_entry,
    test_data
):
    """
    GIVEN a Django application
    WHEN the user requests to update an win entry
    THEN the win entry is updated
    """
    win_entries = WinEntry.objects.all()
    assert len(win_entries) == 0

    current_date = date.today()

    client, user = authenticated_user

    win_entry = add_win_entry(
        title="Finished HTML and CSS",
        user=user,
    )

    test_data["payload"]["user"] = user.id

    res = client.put(
        f"/api/wins/{current_date}/{win_entry.id}/",
        test_data["payload"],
        format="json"
    )

    assert res.status_code == 200
    assert res.data["title"] == test_data["payload"]["title"]

    res_check = client.get(
        f"/api/wins/{current_date}/{win_entry.id}/",
        format="json"
    )

    assert res_check.status_code == 200
    assert res.data["title"] == test_data["payload"]["title"]

    win_entries = WinEntry.objects.all()
    assert len(win_entries) == 1


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
def test_update_win_entry_incorrect_data(
    authenticated_user,
    add_win_entry,
    test_data
):
    """
    GIVEN a Django application
    WHEN the user requests to update an win entry with an incorrect id
    THEN the win entry is not updated
    """
    client, user = authenticated_user

    current_date = date.today()

    add_win_entry(
        title="Finished HTML and CSS",
        user=user,
    )

    win_data = {
        "title": "Finished HTML and CSS",
        "user": user.id,
    }

    res = client.put(
        f"/api/wins/{current_date}/{test_data['incorrect_id']}/",
        win_data,
        format="json"
    )

    print("response data", res)

    assert res.status_code == test_data["expected_status_code"]


@pytest.mark.django_db
@pytest.mark.parametrize("requested_date", [
    "2024-07-06", "2023-03-05", "2022-09-16"
])
def test_update_win_entry_incorrect_date(
    authenticated_user,
    requested_date
):
    """
    GIVEN a Django application
    WHEN the user requests to update an win entry with an incorrect date
    THEN the win entry is not and permission denied
    """
    (client, *_) = authenticated_user

    res = client.put(
        f"/api/wins/{requested_date}/1/",
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
            "title input": "Finished HTML and CSS",
        },
        "expected_status_code": 400
    }
])
def test_update_win_entry_invalid_json(
    authenticated_user,
    add_win_entry,
    test_data
):
    """
    GIVEN a Django application
    WHEN the user requests to update an win entry with invalid JSON
    THEN the win entry is not updated
    """
    client, user = authenticated_user

    current_date = date.today()

    win_entry = add_win_entry(
        title="Dentist",
        user=user,
    )

    res = client.put(
        f"/api/wins/{current_date}/{win_entry.id}/",
        test_data["payload"],
        format="json"
    )

    assert res.status_code == test_data["expected_status_code"]
