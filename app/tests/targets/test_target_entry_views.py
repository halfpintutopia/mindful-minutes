import json
from datetime import date

import pytest
from django.urls import reverse

# https://dennisokeeffe.medium.com/mocking-python-datetime-in-tests-with
# -freezegun-f5532307d6d6
from freezegun import freeze_time
from rest_framework import status

from journal.models import TargetEntry


@pytest.mark.django_db
def test_get_list_of_target_entries(authenticated_user, add_target_entry):
    """
    GIVEN a Django application
    WHEN a user requests a list of all target entries
    THEN the user should receive a list of all target entries
    """
    client, user = authenticated_user

    target_entries = [
        ("Run for 20 minutes.", 1),
        ("Swim 20 lengths", 2),
        ("Read 2 chapters of Eloquent JavaScript", 4),
        ("Watch Kyle Simpson", 3),
    ]

    for target, order in target_entries:
        add_target_entry(user=user, title=target, order=order)

    url = reverse("target-entry-list", args=[user.slug])

    res = client.get(url)

    assert res.status_code == status.HTTP_200_OK


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

    url = reverse("target-entry-date-list", args=[user.slug, current_date])

    res = client.post(
        url, json.dumps(target_data), content_type="application/json"
    )

    assert res.status_code == status.HTTP_201_CREATED
    assert res.data["user"] == user.id
    assert res.data["title"] == "2 minute cold shower"
    assert res.data["order"] == 1

    target_entries = TargetEntry.objects.all()
    assert len(target_entries) == 1


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

    url = reverse("target-entry-date-list", args=[user.slug, current_date])

    res = client.post(
        url, json.dumps(test_data["payload"]), content_type="application/json"
    )
    assert res.status_code == status.HTTP_400_BAD_REQUEST

    target_entries = TargetEntry.objects.all()
    assert len(target_entries) == 0


@pytest.mark.django_db
@pytest.mark.parametrize("date_param", ["2023-07-01", "2023-06-20"])
def test_add_target_entry_not_current_date(authenticated_user, date_param):
    """
    GIVEN a Django application
    WHEN the user attempts to add an target entry on a date,
    that is not the current date
    THEN the target entry is not created
    """
    target_entries = TargetEntry.objects.all()
    assert len(target_entries) == 0

    client, user = authenticated_user

    target_data = {
        "title": "2 minute cold shower",
        "order": 1,
        "user": user.id,
    }

    url = reverse("target-entry-date-list", args=[user.slug, date_param])

    res = client.post(url, target_data, content_type="application/json")

    assert res.status_code == status.HTTP_403_FORBIDDEN

    target_entries = TargetEntry.objects.all()
    assert len(target_entries) == 0


@pytest.mark.django_db
def test_get_single_target_entry(authenticated_user, add_target_entry):
    """
    GIVEN a Django application
    WHEN the user requests to retrieve an target entry
    THEN check that the target entry is retrieved
    """
    current_date = date.today()

    client, user = authenticated_user

    target_entry = add_target_entry(
        title="2 minute cold shower",
        order=1,
        user=user,
    )

    url = reverse(
        "target-entry-detail",
        args=[user.slug, current_date, target_entry.id],
    )

    res = client.get(url, content_type="application/json")

    assert res.status_code == status.HTTP_200_OK
    assert res.data["user"] == user.id
    assert res.data["title"] == "2 minute cold shower"
    assert res.data["order"] == 1


@pytest.mark.django_db
def test_get_single_target_entry_incorrect_id(
    authenticated_user,
):
    """
    GIVEN a Django application
    WHEN the user requests to retrieve an target entry with an incorrect id
    THEN check the target entry is not retrieved
    """
    client, user = authenticated_user

    current_date = date.today()
    invalid_id = 14258

    url = reverse(
        "target-entry-detail",
        args=[user.slug, current_date, invalid_id],
    )

    res = client.get(url)

    assert res.status_code == status.HTTP_404_NOT_FOUND


@pytest.mark.django_db
def test_get_all_target_entries_by_current_date(
    authenticated_user, add_target_entry
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

    url = reverse("target-entry-date-list", args=[user.slug, current_date])

    res = client.get(url)

    assert res.status_code == status.HTTP_200_OK
    assert res.data[0]["created_on"] == str(current_date)

    target_entries = TargetEntry.objects.filter(created_on__date=current_date)
    assert len(target_entries) == 4


@pytest.mark.django_db
@pytest.mark.parametrize(
    "created_on_timestamp",
    [
        "2023-07-06 12:00:00",
        "2023-06-04 10:30:00",
        "2022-07-09 19:45:00",
    ],
)
def test_get_all_target_entries_by_date(
    authenticated_user, add_target_entry, created_on_timestamp
):
    """
    GIVEN a Django application
    WHEN the user requests to retrieve all target entries by date
    THEN check all target entries are retrieved
    """
    date_and_time = created_on_timestamp.split(" ")
    client, user = authenticated_user

    with freeze_time(created_on_timestamp):
        target_entries = TargetEntry.objects.all()
        assert len(target_entries) == 0

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

    url = reverse("target-entry-date-list", args=[user.slug, date_and_time[0]])
    res = client.get(url)

    assert res.status_code == status.HTTP_200_OK
    assert res.data[0]["created_on"] == date_and_time[0]

    target_entries = TargetEntry.objects.filter(
        created_on__date=date_and_time[0]
    )
    assert len(target_entries) == 4


@pytest.mark.django_db
def test_remove_target_entry(authenticated_user, add_target_entry):
    """
    GIVEN a Django application
    WHEN the user requests to remove an target entry
    THEN the target entry is removed
    """
    target_entries = TargetEntry.objects.all()
    assert len(target_entries) == 0

    client, user = authenticated_user

    target_entry = add_target_entry(
        title="2 minute cold shower",
        order=1,
        user=user,
    )

    target_date = target_entry.created_on.strftime("%Y-%m-%d")

    url = reverse(
        "target-entry-detail",
        args=[user.slug, target_date, target_entry.id],
    )

    res = client.get(url, content_type="application/json")

    assert res.status_code == status.HTTP_200_OK
    assert res.data["title"] == "2 minute cold shower"
    assert res.data["order"] == 1

    res_delete = client.delete(url, content_type="application/json")

    assert res_delete.status_code == status.HTTP_204_NO_CONTENT

    url_retrieve = reverse(
        "target-entry-date-list", args=[user.slug, target_date]
    )

    res_retrieve = client.get(url_retrieve, content_type="application/json")

    assert res_retrieve.status_code == status.HTTP_200_OK
    assert len(res_retrieve.data) == 0

    assert not TargetEntry.objects.filter(id=target_entry.id).exists()

    target_entries = TargetEntry.objects.all()
    assert len(target_entries) == 0


@pytest.mark.django_db
def test_remove_target_invalid_id(authenticated_user):
    """
    GIVEN a Django application
    WHEN the user requests to remove an target entry with an invalid id
    THEN the target entry is not removed
    """
    target_entries = TargetEntry.objects.all()
    assert len(target_entries) == 0

    current_date = date.today()
    invalid_id = 12756

    client, user = authenticated_user

    url = reverse(
        "target-entry-detail",
        args=[user.slug, current_date, invalid_id],
    )

    res = client.delete(url, content_type="application/json")

    assert res.status_code == status.HTTP_404_NOT_FOUND

    updated_target_entries = TargetEntry.objects.all()
    assert len(target_entries) == len(updated_target_entries)
    assert len(updated_target_entries) == 0


@pytest.mark.django_db
@pytest.mark.parametrize(
    "requested_date",
    ["2024-07-06 12:00:00", "2023-03-05 15:30:00", "2022-09-16 23:15:00"],
)
def test_remove_target_not_current_date(
    authenticated_user, requested_date, add_target_entry
):
    """
    GIVEN a Django application
    WHEN the user requests to remove an target entry when the date is not
    today
    THEN the target entry is not removed
    """
    target_entries = TargetEntry.objects.all()
    assert len(target_entries) == 0

    client, user = authenticated_user
    date_and_time = requested_date.split(" ")

    with freeze_time(requested_date):
        target_entry = add_target_entry(
            title="2 minute cold shower",
            order=1,
            user=user,
        )

    url = reverse(
        "target-entry-detail",
        args=[user.slug, date_and_time[0], target_entry.id],
    )

    res = client.delete(url, content_type="application/json")

    assert res.status_code == status.HTTP_403_FORBIDDEN

    updated_target_entries = TargetEntry.objects.all()
    assert len(updated_target_entries) == 1


@pytest.mark.django_db
@pytest.mark.parametrize(
    "test_data",
    [
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
        },
    ],
)
def test_update_target_entry(authenticated_user, add_target_entry, test_data):
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

    url = reverse(
        "target-entry-detail",
        args=[user.slug, current_date, target_entry.id],
    )

    res = client.put(
        url, json.dumps(test_data["payload"]), content_type="application/json"
    )

    assert res.status_code == status.HTTP_200_OK
    assert res.data["title"] == test_data["payload"]["title"]
    assert res.data["order"] == test_data["payload"]["order"]

    res_check = client.get(url, content_type="application/json")

    assert res_check.status_code == status.HTTP_200_OK
    assert res.data["title"] == test_data["payload"]["title"]
    assert res.data["order"] == test_data["payload"]["order"]

    target_entries = TargetEntry.objects.all()
    assert len(target_entries) == 1


@pytest.mark.django_db
def test_update_target_entry_incorrect_data(
    authenticated_user, add_target_entry
):
    """
    GIVEN a Django application
    WHEN the user requests to update an target entry with an incorrect id
    THEN the target entry is not updated
    """
    client, user = authenticated_user

    current_date = date.today()
    invalid_id = 12574

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

    url = reverse(
        "target-entry-detail",
        args=[user.slug, current_date, invalid_id],
    )

    res = client.put(
        url, json.dumps(target_data), content_type="application/json"
    )

    assert res.status_code == status.HTTP_404_NOT_FOUND


@pytest.mark.django_db
@pytest.mark.parametrize(
    "requested_date",
    ["2024-07-01 12:00:00", "2023-03-05 06:00:00", "2022-09-16 21:15:00"],
)
def test_update_target_entry_incorrect_date(
    authenticated_user, requested_date, add_target_entry
):
    """
    GIVEN a Django application
    WHEN the user requests to update an target entry with an incorrect date
    THEN the target entry is not and permission denied
    """
    date_and_time = requested_date.split(" ")

    client, user = authenticated_user

    with freeze_time(requested_date):
        target_entry = add_target_entry(
            title="2 minute cold shower",
            order=1,
            user=user,
        )

    url = reverse(
        "target-entry-detail",
        args=[user.slug, date_and_time[0], target_entry.id],
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
                "title input": "2 minute cold shower",
                "order": 1,
            },
        },
    ],
)
def test_update_target_entry_invalid_json(
    authenticated_user, add_target_entry, test_data
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

    url = reverse(
        "target-entry-detail",
        args=[user.slug, current_date, target_entry.id],
    )

    res = client.put(
        url, test_data["payload"], content_type="application/json"
    )

    assert res.status_code == status.HTTP_400_BAD_REQUEST
