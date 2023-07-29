import json
from datetime import date

import pytest
from django.urls import reverse

# https://dennisokeeffe.medium.com/mocking-python-datetime-in-tests-with
# -freezegun-f5532307d6d6
from freezegun import freeze_time
from rest_framework import status

from journal.models import NoteEntry


@pytest.mark.django_db
def test_get_list_of_note_entries(authenticated_user, add_note_entry):
    """
    GIVEN a Django application
    WHEN a user requests a list of all note entries
    THEN the user should receive a list of all note entries
    """
    client, user = authenticated_user

    note_entries = [
        "Move dentist appointment.",
        "Set up printer.",
        "Order book.",
        "Join Meetup in Zurich",
    ]

    for note in note_entries:
        add_note_entry(user=user, content=note)

    url = reverse("note-entry-list", args=[user.slug])

    res = client.get(url)

    assert res.status_code == status.HTTP_200_OK


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

    url = reverse("note-entry-date-list", args=[user.slug, current_date])

    res = client.post(
        url, json.dumps(note_data), content_type="application/json"
    )

    assert res.status_code == status.HTTP_201_CREATED
    assert res.data["user"] == user.id
    assert res.data["content"] == "I have to pick up books from Library."

    note_entries = NoteEntry.objects.all()
    assert len(note_entries) == 1


@pytest.mark.django_db
@pytest.mark.parametrize(
    "test_data",
    [
        {"payload": {}, "status_code": 400},
        {
            "payload": {
                "content entry": "I have to pick up books from Library.",
            },
            "status_code": 400,
        },
    ],
)
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

    url = reverse("note-entry-date-list", args=[user.slug, current_date])

    res = client.post(
        url, json.dumps(test_data["payload"]), content_type="application/json"
    )
    assert res.status_code == status.HTTP_400_BAD_REQUEST

    note_entries = NoteEntry.objects.all()
    assert len(note_entries) == 0


@pytest.mark.django_db
@pytest.mark.parametrize("date_param", ["2023-07-01", "2023-06-20"])
def test_add_note_entry_not_current_date(authenticated_user, date_param):
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

    url = reverse("note-entry-date-list", args=[user.slug, date_param])

    res = client.post(url, note_data, content_type="application/json")

    assert res.status_code == status.HTTP_403_FORBIDDEN

    note_entries = NoteEntry.objects.all()
    assert len(note_entries) == 0


@pytest.mark.django_db
def test_get_single_note_entry(authenticated_user, add_note_entry):
    """
    GIVEN a Django application
    WHEN the user requests to retrieve an note entry
    THEN check that the note entry is retrieved
    """
    current_date = date.today()

    client, user = authenticated_user

    note_entry = add_note_entry(
        content="I have to pick up books from Library.",
        user=user,
    )

    url = reverse(
        "note-entry-detail",
        args=[user.slug, current_date, note_entry.id],
    )

    res = client.get(url, content_type="application/json")

    assert res.status_code == status.HTTP_200_OK
    assert res.data["user"] == user.id
    assert res.data["content"] == "I have to pick up books from Library."


@pytest.mark.django_db
def test_get_single_note_entry_incorrect_id(
    authenticated_user,
):
    """
    GIVEN a Django application
    WHEN the user requests to retrieve an note entry with an incorrect id
    THEN check the note entry is not retrieved
    """
    client, user = authenticated_user

    current_date = date.today()
    invalid_id = 14258

    url = reverse(
        "note-entry-detail", args=[user.slug, current_date, invalid_id]
    )

    res = client.get(url)

    assert res.status_code == status.HTTP_404_NOT_FOUND


@pytest.mark.django_db
def test_get_all_note_entries_by_current_date(
    authenticated_user, add_note_entry
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

    url = reverse("note-entry-date-list", args=[user.slug, current_date])

    res = client.get(url)

    assert res.status_code == status.HTTP_200_OK
    assert res.data[0]["created_on"] == str(current_date)

    note_entries = NoteEntry.objects.filter(created_on__date=current_date)
    assert len(note_entries) == 1


@pytest.mark.django_db
@pytest.mark.parametrize(
    "created_on_timestamp",
    [
        "2023-07-06 12:00:00",
        "2023-06-04 10:30:00",
        "2022-07-09 19:45:00",
    ],
)
def test_get_all_note_entries_by_date(
    authenticated_user, add_note_entry, created_on_timestamp
):
    """
    GIVEN a Django application
    WHEN the user requests to retrieve all note entries by date
    THEN check all note entries are retrieved
    """
    date_and_time = created_on_timestamp.split(" ")
    client, user = authenticated_user

    with freeze_time(created_on_timestamp):
        note_entries = NoteEntry.objects.all()
        assert len(note_entries) == 0

        add_note_entry(
            content="I have to pick up books from Library.",
            user=user,
        )

    url = reverse("note-entry-date-list", args=[user.slug, date_and_time[0]])
    res = client.get(url)

    assert res.status_code == status.HTTP_200_OK
    assert res.data[0]["created_on"] == date_and_time[0]

    note_entries = NoteEntry.objects.filter(created_on__date=date_and_time[0])
    assert len(note_entries) == 1


@pytest.mark.django_db
def test_remove_note_entry(authenticated_user, add_note_entry):
    """
    GIVEN a Django application
    WHEN the user requests to remove an note entry
    THEN the note entry is removed
    """
    note_entries = NoteEntry.objects.all()
    assert len(note_entries) == 0

    client, user = authenticated_user

    note_entry = add_note_entry(
        content="I have to pick up books from Library.",
        user=user,
    )

    note_date = note_entry.created_on.strftime("%Y-%m-%d")

    url = reverse(
        "note-entry-detail", args=[user.slug, note_date, note_entry.id]
    )

    res = client.get(url, content_type="application/json")

    assert res.status_code == status.HTTP_200_OK
    assert res.data["content"] == "I have to pick up books from Library."

    res_delete = client.delete(url, content_type="application/json")

    assert res_delete.status_code == status.HTTP_204_NO_CONTENT

    url_retrieve = reverse("note-entry-date-list", args=[user.slug, note_date])

    res_retrieve = client.get(url_retrieve, content_type="application/json")

    assert res_retrieve.status_code == status.HTTP_200_OK
    assert len(res_retrieve.data) == 0

    assert not NoteEntry.objects.filter(id=note_entry.id).exists()

    note_entries = NoteEntry.objects.all()
    assert len(note_entries) == 0


@pytest.mark.django_db
def test_remove_note_invalid_id(authenticated_user):
    """
    GIVEN a Django application
    WHEN the user requests to remove an note entry with an invalid id
    THEN the note entry is not removed
    """
    note_entries = NoteEntry.objects.all()
    assert len(note_entries) == 0

    current_date = date.today()
    invalid_id = 12756

    client, user = authenticated_user

    url = reverse(
        "note-entry-detail", args=[user.slug, current_date, invalid_id]
    )

    res = client.delete(url, content_type="application/json")

    assert res.status_code == status.HTTP_404_NOT_FOUND

    updated_note_entries = NoteEntry.objects.all()
    assert len(note_entries) == len(updated_note_entries)
    assert len(updated_note_entries) == 0


@pytest.mark.django_db
@pytest.mark.parametrize(
    "requested_date",
    ["2024-07-06 12:00:00", "2023-03-05 15:30:00", "2022-09-16 23:15:00"],
)
def test_remove_note_not_current_date(
    authenticated_user, requested_date, add_note_entry
):
    """
    GIVEN a Django application
    WHEN the user requests to remove an note entry when the date is not today
    THEN the note entry is not removed
    """
    note_entries = NoteEntry.objects.all()
    assert len(note_entries) == 0

    client, user = authenticated_user
    date_and_time = requested_date.split(" ")

    with freeze_time(requested_date):
        note_entry = add_note_entry(
            content="I have to pick up books from Library.",
            user=user,
        )

    url = reverse(
        "note-entry-detail",
        args=[user.slug, date_and_time[0], note_entry.id],
    )

    res = client.delete(url, content_type="application/json")

    assert res.status_code == status.HTTP_403_FORBIDDEN

    updated_note_entries = NoteEntry.objects.all()
    assert len(updated_note_entries) == 1


@pytest.mark.django_db
@pytest.mark.parametrize(
    "test_data",
    [
        {
            "payload": {
                "content": "20 minutes meditation.",
            }
        },
        {
            "payload": {
                "content": "I have to pick up books from Library.",
            }
        },
    ],
)
def test_update_note_entry(authenticated_user, add_note_entry, test_data):
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

    url = reverse(
        "note-entry-detail",
        args=[user.slug, current_date, note_entry.id],
    )

    res = client.put(
        url, json.dumps(test_data["payload"]), content_type="application/json"
    )

    assert res.status_code == status.HTTP_200_OK
    assert res.data["content"] == test_data["payload"]["content"]

    res_check = client.get(url, content_type="application/json")

    assert res_check.status_code == status.HTTP_200_OK
    assert res.data["content"] == test_data["payload"]["content"]

    note_entries = NoteEntry.objects.all()
    assert len(note_entries) == 1


@pytest.mark.django_db
def test_update_note_entry_incorrect_data(authenticated_user, add_note_entry):
    """
    GIVEN a Django application
    WHEN the user requests to update an note entry with an incorrect id
    THEN the note entry is not updated
    """
    client, user = authenticated_user

    current_date = date.today()
    invalid_id = 12574

    add_note_entry(
        content="I have to pick up books from Library.",
        user=user,
    )

    note_data = {
        "content": "I have to pick up books from Library.",
        "user": user.id,
    }

    url = reverse(
        "note-entry-detail", args=[user.slug, current_date, invalid_id]
    )

    res = client.put(
        url, json.dumps(note_data), content_type="application/json"
    )

    assert res.status_code == status.HTTP_404_NOT_FOUND


@pytest.mark.django_db
@pytest.mark.parametrize(
    "requested_date",
    ["2024-07-01 12:00:00", "2023-03-05 06:00:00", "2022-09-16 21:15:00"],
)
def test_update_note_entry_incorrect_date(
    authenticated_user, requested_date, add_note_entry
):
    """
    GIVEN a Django application
    WHEN the user requests to update an note entry with an incorrect date
    THEN the note entry is not and permission denied
    """
    date_and_time = requested_date.split(" ")

    client, user = authenticated_user

    with freeze_time(requested_date):
        note_entry = add_note_entry(
            content="I have to pick up books from Library.",
            user=user,
        )

    url = reverse(
        "note-entry-detail",
        args=[user.slug, date_and_time[0], note_entry.id],
    )

    res = client.put(url, content_type="application/json")

    assert res.status_code == status.HTTP_403_FORBIDDEN


@pytest.mark.django_db
@pytest.mark.parametrize(
    "test_data",
    [
        {
            "payload": {},
        },
        {
            "payload": {
                "content entry": "I have to pick up books from Library.",
            },
        },
    ],
)
def test_update_note_entry_invalid_json(
    authenticated_user, add_note_entry, test_data
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

    url = reverse(
        "note-entry-detail",
        args=[user.slug, current_date, note_entry.id],
    )

    res = client.put(
        url, test_data["payload"], content_type="application/json"
    )

    assert res.status_code == status.HTTP_400_BAD_REQUEST
