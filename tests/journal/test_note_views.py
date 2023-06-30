from datetime import date
# https://dennisokeeffe.medium.com/mocking-python-datetime-in-tests-with-freezegun-f5532307d6d6
from freezegun import freeze_time

import pytest

from journal.models import NoteEntry


@pytest.mark.django_db
def test_add_note_entry(authenticated_user):
    """
    GIVEN a Django application
    WHEN the user requests to add an note entry
    THEN check that the note entry is added
    """
    note_entries = NoteEntry.objects.all()
    assert len(note_entries) == 0

    current_date = date.today()

    client, user = authenticated_user

    note_data = {
        "content": "I have to pick up books from Library.",
        "user": user.id,
    }

    res = client.post(
        f"/api/notes/{current_date}/",
        note_data,
        format="json"
    )

    assert res.status_code == 201
    assert res.data["user"] == user.id
    assert res.data["content"] == "I have to pick up books from Library."

    note_entries = NoteEntry.objects.all()
    assert len(note_entries) == 1


@pytest.mark.django_db
@pytest.mark.parametrize("test_data", [
    {
        "payload": {},
        "status_code": 400
    },
    {
        "payload": {
            "content entry": "I have to pick up books from Library.",
        },
        "status_code": 400
    }
])
def test_add_note_entry_incorrect_json(authenticated_user, test_data):
    """
    GIVEN a Django application
    WHEN the user requests to add an note entry with an invalid payload
    THEN the payload is not sent
    """
    note_entries = NoteEntry.objects.all()
    assert len(note_entries) == 0

    current_date = date.today()

    client, user = authenticated_user

    test_data["payload"]["user"] = user.id

    res = client.post(
        f"/api/notes/{current_date}/",
        test_data["payload"],
        format="json"
    )
    assert res.status_code == 400

    note_entries = NoteEntry.objects.all()
    assert len(note_entries) == 0


@pytest.mark.django_db
@pytest.mark.parametrize("date_param", ["2023-07-01", "2023-06-20"])
def test_add_note_entry_not_current_date(
    authenticated_user,
    date_param
):
    """
    GIVEN a Django application
    WHEN the user attempts to add an note entry on a date,
    that is not the current date
    THEN the note entry is not created
    """
    note_entries = NoteEntry.objects.all()
    assert len(note_entries) == 0

    client, user = authenticated_user

    note_data = {
        "content": "I have to pick up books from Library.",
        "user": user.id,
    }

    res = client.post(
        f"/api/notes/{date_param}/",
        note_data,
        format="json"
    )

    assert res.status_code == 403

    note_entries = NoteEntry.objects.all()
    assert len(note_entries) == 0


@pytest.mark.django_db
def test_get_single_note_entry(
    authenticated_user,
    add_note_entry
):
    """
    GIVEN a Django application
    WHEN the user requests to retrieve an note entry
    THEN check that the note entry is retrieved
    """
    current_date = date.today()

    client, user = authenticated_user

    note = add_note_entry(
        content="I have to pick up books from Library.",
        user=user,
    )

    res = client.get(
        f"/api/notes/{current_date}/{note.id}/",
        format="json"
    )

    assert res.status_code == 200
    assert res.data["user"] == user.id
    assert res.data["content"] == "I have to pick up books from Library."


@pytest.mark.django_db
@pytest.mark.parametrize("invalid_id", ["random", "1", 14258])
def test_get_single_note_entry_incorrect_id(
    authenticated_user,
    invalid_id
):
    """
    GIVEN a Django application
    WHEN the user requests to retrieve an note entry with an incorrect id
    THEN check the note entry is not retrieved
    """
    (client, *_) = authenticated_user

    current_date = date.today()

    res = client.get(f"/api/notes/{current_date}/{invalid_id}/")

    assert res.status_code == 404


@pytest.mark.django_db
def test_get_all_note_entries_by_current_date(
    authenticated_user,
    add_note_entry
):
    """
    GIVEN a Django application
    WHEN the user requests to retrieve all note entries
    by current date
    THEN check all note entries are retrieved
    """
    note_entries = NoteEntry.objects.all()
    assert len(note_entries) == 0

    current_date = date.today()

    client, user = authenticated_user

    add_note_entry(
        content="I have to pick up books from Library.",
        user=user,
    )

    res = client.get(f"/api/notes/{str(current_date)}/")

    assert res.status_code == 200
    assert res.data[0]["created_on"] == str(current_date)

    note_entries = NoteEntry.objects.filter(
        created_on__date=current_date)
    assert len(note_entries) == 1


@pytest.mark.django_db
@pytest.mark.parametrize("created_on_timestamp", [
    "2023-07-06 12:00:00",
    "2023-06-04 10:30:00",
    "2022-07-09 19:45:00",
])
def test_get_all_note_entries_by_date(
    authenticated_user,
    add_note_entry,
    created_on_timestamp
):
    """
    GIVEN a Django application
    WHEN the user requests to retrieve all note entries by date
    THEN check all note entries are retrieved
    """
    with freeze_time(created_on_timestamp):
        note_entries = NoteEntry.objects.all()
        assert len(note_entries) == 0

        current_date = date.today()

        client, user = authenticated_user

        add_note_entry(
            content="I have to pick up books from Library.",
            user=user,
        )

        res = client.get(f"/api/notes/{str(current_date)}/")

        assert res.status_code == 200
        assert res.data[0]["created_on"] == str(current_date)

        note_entries = NoteEntry.objects.filter(
            created_on__date=current_date)
        assert len(note_entries) == 1


@pytest.mark.django_db
def test_remove_note_entry(
    authenticated_user,
    add_note_entry
):
    """
    GIVEN a Django application
    WHEN the user requests to remove an note entry
    THEN the note entry is removed
    """
    note_entries = NoteEntry.objects.all()
    assert len(note_entries) == 0

    current_date = date.today()

    client, user = authenticated_user

    note_entry = add_note_entry(
        content="I have to pick up books from Library.",
        user=user,
    )

    res = client.get(
        f"/api/notes/{current_date}/{note_entry.id}/",
        format="json"
    )

    assert res.status_code == 200
    assert res.data["content"] == "I have to pick up books from Library."

    res_delete = client.delete(
        f"/api/notes/{current_date}/{note_entry.id}/",
        format="json"
    )

    assert res_delete.status_code == 204

    res_retrieve = client.get(
        f"/api/notes/{current_date}/", format="json")

    assert res_retrieve.status_code == 200
    assert len(res_retrieve.data) == 0

    assert not NoteEntry.objects.filter(id=note_entry.id).exists()

    note_entries = NoteEntry.objects.all()
    assert len(note_entries) == 0


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
def test_remove_note_invalid_id(
    authenticated_user,
    test_data
):
    """
    GIVEN a Django application
    WHEN the user requests to remove an note entry with an invalid id
    THEN the note entry is not removed
    """
    note_entries = NoteEntry.objects.all()
    assert len(note_entries) == 0

    current_date = date.today()

    (client, *_) = authenticated_user

    res = client.delete(
        f"/api/notes/{current_date}/{test_data['incorrect_id']}/",
        format="json"
    )

    assert res.status_code == test_data["expected_status_code"]

    updated_note_entries = NoteEntry.objects.all()
    assert len(note_entries) == len(updated_note_entries)
    assert len(updated_note_entries) == 0


@pytest.mark.django_db
@pytest.mark.parametrize("requested_date", [
    "2023-07-06", "2023-03-05", "2022-09-16"
])
def test_remove_note_not_current_date(
    authenticated_user, requested_date
):
    """
    GIVEN a Django application
    WHEN the user requests to remove an note entry when the date is not today
    THEN the note entry is not removed
    """
    note_entries = NoteEntry.objects.all()
    assert len(note_entries) == 0

    (client, *_) = authenticated_user

    res = client.delete(
        f"/api/notes/{requested_date}/1/", format="json")

    assert res.status_code == 403

    updated_note_entries = NoteEntry.objects.all()
    assert len(note_entries) == len(updated_note_entries)
    assert len(updated_note_entries) == 0


@pytest.mark.django_db
@pytest.mark.parametrize("test_data", [
    {
        "payload": {
            "content": "20 minutes meditation",
        }
    },
    {
        "payload": {
            "content": "I have to pick up books from Library.",
        }
    },
    {
        "payload": {
            "content": "20 minutes meditation",
        }
    }
])
def test_update_note_entry(
    authenticated_user,
    add_note_entry,
    test_data
):
    """
    GIVEN a Django application
    WHEN the user requests to update an note entry
    THEN the note entry is updated
    """
    note_entries = NoteEntry.objects.all()
    assert len(note_entries) == 0

    current_date = date.today()

    client, user = authenticated_user

    note_entry = add_note_entry(
        content="I have to pick up books from Library.",
        user=user,
    )

    test_data["payload"]["user"] = user.id

    res = client.put(
        f"/api/notes/{current_date}/{note_entry.id}/",
        test_data["payload"],
        format="json"
    )

    assert res.status_code == 200
    assert res.data["content"] == test_data["payload"]["content"]

    res_check = client.get(
        f"/api/notes/{current_date}/{note_entry.id}/",
        format="json"
    )

    assert res_check.status_code == 200
    assert res.data["content"] == test_data["payload"]["content"]

    note_entries = NoteEntry.objects.all()
    assert len(note_entries) == 1


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
def test_update_note_entry_incorrect_data(
    authenticated_user,
    add_note_entry,
    test_data
):
    """
    GIVEN a Django application
    WHEN the user requests to update an note entry with an incorrect id
    THEN the note entry is not updated
    """
    client, user = authenticated_user

    current_date = date.today()

    add_note_entry(
        content="I have to pick up books from Library.",
        user=user,
    )

    note_data = {
        "content": "I have to pick up books from Library.",
        "user": user.id,
    }

    res = client.put(
        f"/api/notes/{current_date}/{test_data['incorrect_id']}/",
        note_data,
        format="json"
    )

    print("response data", res)

    assert res.status_code == test_data["expected_status_code"]


@pytest.mark.django_db
@pytest.mark.parametrize("requested_date", [
    "2023-07-06", "2023-03-05", "2022-09-16"
])
def test_update_note_entry_incorrect_date(
    authenticated_user,
    requested_date
):
    """
    GIVEN a Django application
    WHEN the user requests to update an note entry with an incorrect date
    THEN the note entry is not and permission denied
    """
    (client, *_) = authenticated_user

    res = client.put(
        f"/api/notes/{requested_date}/1/",
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
            "content entry": "I have to pick up books from Library.",
        },
        "expected_status_code": 400
    }
])
def test_update_note_entry_invalid_json(
    authenticated_user,
    add_note_entry,
    test_data
):
    """
    GIVEN a Django application
    WHEN the user requests to update an note entry with invalid JSON
    THEN the note entry is not updated
    """
    client, user = authenticated_user

    current_date = date.today()

    note_entry = add_note_entry(
        content="Dentist",
        user=user,
    )

    res = client.put(
        f"/api/notes/{current_date}/{note_entry.id}/",
        test_data["payload"],
        format="json"
    )

    assert res.status_code == test_data["expected_status_code"]
