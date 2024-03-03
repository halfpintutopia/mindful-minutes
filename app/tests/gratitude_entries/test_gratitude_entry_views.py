import json
from datetime import date

import pytest
from django.urls import reverse
from freezegun import freeze_time
from rest_framework import status

from gratitude_entries.models import GratitudeEntry


@pytest.mark.django_db
def test_get_list_of_gratitude_entries(authenticated_user, add_gratitude_entry):
    """
    GIVEN a Django application
    WHEN a user requests a list of all gratitude entries
    THEN the user should receive a list of all gratitude entries
    """
    client, user = authenticated_user

    gratitude_entries = [
        "I am healthy.",
        "Thanks for a beautiful day.",
        "I handed in my assignment",
        "I received a 85% pass mark.",
        "Celebration of the arrival of healthy twins.",
    ]

    for gratitude in gratitude_entries:
        add_gratitude_entry(user=user, content=gratitude)

    url = reverse("gratitude-entry-list", args=[user.slug])

    res = client.get(url)

    assert res.status_code == status.HTTP_200_OK


@pytest.mark.django_db
def test_add_gratitude_entry(authenticated_user):
    """
    GIVEN a Django application
    WHEN the user requests to add a gratitude entry
    THEN check that the gratitude entry is added
    """
    gratitude_entries = GratitudeEntry.objects.all()
    assert len(gratitude_entries) == 0

    current_date = date.today()

    client, user = authenticated_user

    gratitude_data = {
        "content": "I am healthy. My studies are going well. I am free and "
        "strong.",
        "user": user.id,
    }

    url = reverse("gratitude-entry-date-list", args=[user.slug, current_date])

    res = client.post(
        url, json.dumps(gratitude_data), content_type="application/json"
    )

    assert res.status_code == status.HTTP_201_CREATED
    assert res.data["user"] == user.id
    assert (
        res.data["content"] == "I am healthy. My studies are going well. I am "
        ""
        "free and strong."
    )

    gratitude_entries = GratitudeEntry.objects.all()
    assert len(gratitude_entries) == 1


@pytest.mark.django_db
@pytest.mark.parametrize(
    "test_data",
    [
        {"payload": {}, "status_code": 400},
        {
            "payload": {
                "content entry": "I am healthy. My studies are going well. I "
                "am free and strong.",
            },
            "status_code": 400,
        },
    ],
)
def test_add_gratitude_entry_incorrect_json(authenticated_user, test_data):
    """
    GIVEN a Django application
    WHEN the user requests to add a gratitude entry with an invalid payload
    THEN the payload is not sent
    """
    gratitude_entries = GratitudeEntry.objects.all()
    assert len(gratitude_entries) == 0

    current_date = date.today()

    client, user = authenticated_user

    test_data["payload"]["user"] = user.id

    url = reverse("gratitude-entry-date-list", args=[user.slug, current_date])

    res = client.post(
        url, json.dumps(test_data["payload"]), content_type="application/json"
    )
    assert res.status_code == status.HTTP_400_BAD_REQUEST

    gratitude_entries = GratitudeEntry.objects.all()
    assert len(gratitude_entries) == 0


@pytest.mark.django_db
@pytest.mark.parametrize("date_param", ["2023-07-01", "2023-06-20"])
def test_add_gratitude_entry_not_current_date(authenticated_user, date_param):
    """
    GIVEN a Django application
    WHEN the user attempts to add a gratitude entry on a date,
    that is not the current date
    THEN the gratitude entry is not created
    """
    gratitude_entries = GratitudeEntry.objects.all()
    assert len(gratitude_entries) == 0

    client, user = authenticated_user

    gratitude_data = {
        "content": "I am healthy. My studies are going well. I am free and "
        "strong.",
        "user": user.id,
    }

    url = reverse("gratitude-entry-date-list", args=[user.slug, date_param])

    res = client.post(url, gratitude_data, content_type="application/json")

    assert res.status_code == status.HTTP_403_FORBIDDEN

    gratitude_entries = GratitudeEntry.objects.all()
    assert len(gratitude_entries) == 0


@pytest.mark.django_db
def test_get_single_gratitude_entry(authenticated_user, add_gratitude_entry):
    """
    GIVEN a Django application
    WHEN the user requests to retrieve a gratitude entry
    THEN check that the gratitude entry is retrieved
    """
    current_date = date.today()

    client, user = authenticated_user

    gratitude_entry = add_gratitude_entry(
        content="I am healthy. My studies are going well. I am free and "
        "strong.",
        user=user,
    )

    url = reverse(
        "gratitude-entry-detail",
        args=[user.slug, current_date, gratitude_entry.id],
    )

    res = client.get(url, content_type="application/json")

    assert res.status_code == status.HTTP_200_OK
    assert res.data["user"] == user.id
    assert (
        res.data["content"] == "I am healthy. My studies are going well. I am "
        ""
        "free and strong."
    )


@pytest.mark.django_db
def test_get_single_gratitude_entry_incorrect_id(
    authenticated_user,
):
    """
    GIVEN a Django application
    WHEN the user requests to retrieve a gratitude entry with an incorrect id
    THEN check the gratitude entry is not retrieved
    """
    client, user = authenticated_user

    current_date = date.today()
    invalid_id = 14258

    url = reverse(
        "gratitude-entry-detail",
        args=[user.slug, current_date, invalid_id],
    )

    res = client.get(url)

    assert res.status_code == status.HTTP_404_NOT_FOUND


@pytest.mark.django_db
def test_get_all_gratitude_entries_by_current_date(
    authenticated_user, add_gratitude_entry
):
    """
    GIVEN a Django application
    WHEN the user requests to retrieve all gratitude entries
    by current date
    THEN check all gratitude entries are retrieved
    """
    gratitude_entries = GratitudeEntry.objects.all()
    assert len(gratitude_entries) == 0

    current_date = date.today()

    client, user = authenticated_user

    add_gratitude_entry(
        content="I am healthy. My studies are going well. I am free and "
        "strong.",
        user=user,
    )

    url = reverse("gratitude-entry-date-list", args=[user.slug, current_date])

    res = client.get(url)

    assert res.status_code == status.HTTP_200_OK
    assert res.data[0]["created_on"] == str(current_date)

    gratitude_entries = GratitudeEntry.objects.filter(
        created_on__date=current_date
    )
    assert len(gratitude_entries) == 1


@pytest.mark.django_db
@pytest.mark.parametrize(
    "created_on_timestamp",
    [
        "2023-07-06 12:00:00",
        "2023-06-04 10:30:00",
        "2022-07-09 19:45:00",
    ],
)
def test_get_all_gratitude_entries_by_date(
    authenticated_user, add_gratitude_entry, created_on_timestamp
):
    """
    GIVEN a Django application
    WHEN the user requests to retrieve all gratitude entries by date
    THEN check all gratitude entries are retrieved
    """
    date_and_time = created_on_timestamp.split(" ")
    client, user = authenticated_user

    with freeze_time(created_on_timestamp):
        gratitude_entries = GratitudeEntry.objects.all()
        assert len(gratitude_entries) == 0

        add_gratitude_entry(
            content="I am healthy. My studies are going well. I am free and "
            ""
            "strong.",
            user=user,
        )

    url = reverse(
        "gratitude-entry-date-list", args=[user.slug, date_and_time[0]]
    )
    res = client.get(url)

    assert res.status_code == status.HTTP_200_OK
    assert res.data[0]["created_on"] == date_and_time[0]

    gratitude_entries = GratitudeEntry.objects.filter(
        created_on__date=date_and_time[0]
    )
    assert len(gratitude_entries) == 1


@pytest.mark.django_db
def test_remove_gratitude_entry(authenticated_user, add_gratitude_entry):
    """
    GIVEN a Django application
    WHEN the user requests to remove a gratitude entry
    THEN the gratitude entry is removed
    """
    gratitude_entries = GratitudeEntry.objects.all()
    assert len(gratitude_entries) == 0

    client, user = authenticated_user

    gratitude_entry = add_gratitude_entry(
        content="I am healthy. My studies are going well. I am free and "
        "strong.",
        user=user,
    )

    gratitude_date = gratitude_entry.created_on.strftime("%Y-%m-%d")

    url = reverse(
        "gratitude-entry-detail",
        args=[user.slug, gratitude_date, gratitude_entry.id],
    )

    res = client.get(url, content_type="application/json")

    assert res.status_code == status.HTTP_200_OK
    assert (
        res.data["content"] == "I am healthy. My studies are going well. I am "
        ""
        "free and strong."
    )

    res_delete = client.delete(url, content_type="application/json")

    assert res_delete.status_code == status.HTTP_204_NO_CONTENT

    url_retrieve = reverse(
        "gratitude-entry-date-list", args=[user.slug, gratitude_date]
    )

    res_retrieve = client.get(url_retrieve, content_type="application/json")

    assert res_retrieve.status_code == status.HTTP_200_OK
    assert len(res_retrieve.data) == 0

    assert not GratitudeEntry.objects.filter(id=gratitude_entry.id).exists()

    gratitude_entries = GratitudeEntry.objects.all()
    assert len(gratitude_entries) == 0


@pytest.mark.django_db
def test_remove_gratitude_invalid_id(authenticated_user):
    """
    GIVEN a Django application
    WHEN the user requests to remove a gratitude entry with an invalid id
    THEN the gratitude entry is not removed
    """
    gratitude_entries = GratitudeEntry.objects.all()
    assert len(gratitude_entries) == 0

    current_date = date.today()
    invalid_id = 12756

    client, user = authenticated_user

    url = reverse(
        "gratitude-entry-detail",
        args=[user.slug, current_date, invalid_id],
    )

    res = client.delete(url, content_type="application/json")

    assert res.status_code == status.HTTP_404_NOT_FOUND

    updated_gratitude_entries = GratitudeEntry.objects.all()
    assert len(gratitude_entries) == len(updated_gratitude_entries)
    assert len(updated_gratitude_entries) == 0


@pytest.mark.django_db
@pytest.mark.parametrize(
    "requested_date",
    ["2024-07-06 12:00:00", "2023-03-05 15:30:00", "2022-09-16 23:15:00"],
)
def test_remove_gratitude_not_current_date(
    authenticated_user, requested_date, add_gratitude_entry
):
    """
    GIVEN a Django application
    WHEN the user requests to remove a gratitude entry when the date is not
    today
    THEN the gratitude entry is not removed
    """
    gratitude_entries = GratitudeEntry.objects.all()
    assert len(gratitude_entries) == 0

    client, user = authenticated_user
    date_and_time = requested_date.split(" ")

    with freeze_time(requested_date):
        gratitude_entry = add_gratitude_entry(
            content="I am healthy. My studies are going well. I am free and "
            ""
            "strong.",
            user=user,
        )

    url = reverse(
        "gratitude-entry-detail",
        args=[user.slug, date_and_time[0], gratitude_entry.id],
    )

    res = client.delete(url, content_type="application/json")

    assert res.status_code == status.HTTP_403_FORBIDDEN

    updated_gratitude_entries = GratitudeEntry.objects.all()
    assert len(updated_gratitude_entries) == 1


@pytest.mark.django_db
@pytest.mark.parametrize(
    "test_data",
    [
        {
            "payload": {
                "content": "I am healthy. My studies are going well. I am "
                "free and strong. Refactored code with new "
                "gratitude",
            }
        },
        {
            "payload": {
                "content": "Read a chapter of Eloquent JavaScript and was "
                "able to explain this to another colleague",
            }
        },
    ],
)
def test_update_gratitude_entry(
    authenticated_user, add_gratitude_entry, test_data
):
    """
    GIVEN a Django application
    WHEN the user requests to update a gratitude entry
    THEN the gratitude entry is updated
    """
    gratitude_entries = GratitudeEntry.objects.all()
    assert len(gratitude_entries) == 0

    current_date = date.today()

    client, user = authenticated_user

    gratitude_entry = add_gratitude_entry(
        content="I am healthy. My studies are going well. I am free and "
        "strong.",
        user=user,
    )

    test_data["payload"]["user"] = user.id

    url = reverse(
        "gratitude-entry-detail",
        args=[user.slug, current_date, gratitude_entry.id],
    )

    res = client.put(
        url, json.dumps(test_data["payload"]), content_type="application/json"
    )

    assert res.status_code == status.HTTP_200_OK
    assert res.data["content"] == test_data["payload"]["content"]

    res_check = client.get(url, content_type="application/json")

    assert res_check.status_code == status.HTTP_200_OK
    assert res.data["content"] == test_data["payload"]["content"]

    gratitude_entries = GratitudeEntry.objects.all()
    assert len(gratitude_entries) == 1


@pytest.mark.django_db
def test_update_gratitude_entry_incorrect_data(
    authenticated_user, add_gratitude_entry
):
    """
    GIVEN a Django application
    WHEN the user requests to update a gratitude entry with an incorrect id
    THEN the gratitude entry is not updated
    """
    client, user = authenticated_user

    current_date = date.today()
    invalid_id = 12574

    add_gratitude_entry(
        content="I am healthy. My studies are going well. I am free and "
        "strong.",
        user=user,
    )

    gratitude_data = {
        "content": "Read a chapter of Eloquent JavaScript and was able to "
        "explain this to another colleague",
        "user": user.id,
    }

    url = reverse(
        "gratitude-entry-detail",
        args=[user.slug, current_date, invalid_id],
    )

    res = client.put(
        url, json.dumps(gratitude_data), content_type="application/json"
    )

    assert res.status_code == status.HTTP_404_NOT_FOUND


@pytest.mark.django_db
@pytest.mark.parametrize(
    "requested_date",
    ["2024-07-01 12:00:00", "2023-03-05 06:00:00", "2022-09-16 21:15:00"],
)
def test_update_gratitude_entry_incorrect_date(
    authenticated_user, requested_date, add_gratitude_entry
):
    """
    GIVEN a Django application
    WHEN the user requests to update a gratitude entry with an incorrect date
    THEN the gratitude entry is not and permission denied
    """
    date_and_time = requested_date.split(" ")

    client, user = authenticated_user

    with freeze_time(requested_date):
        gratitude_entry = add_gratitude_entry(
            content="I am healthy. My studies are going well. I am free and "
            ""
            "strong.",
            user=user,
        )

    url = reverse(
        "gratitude-entry-detail",
        args=[user.slug, date_and_time[0], gratitude_entry.id],
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
                "content entry": "I am healthy. My studies are going well. I "
                "am free and strong.",
            },
        },
    ],
)
def test_update_gratitude_entry_invalid_json(
    authenticated_user, add_gratitude_entry, test_data
):
    """
    GIVEN a Django application
    WHEN the user requests to update a gratitude entry with invalid JSON
    THEN the gratitude entry is not updated
    """
    client, user = authenticated_user

    current_date = date.today()

    gratitude_entry = add_gratitude_entry(
        content="Dentist",
        user=user,
    )

    url = reverse(
        "gratitude-entry-detail",
        args=[user.slug, current_date, gratitude_entry.id],
    )

    res = client.put(url, test_data["payload"], content_type="application/json")

    assert res.status_code == status.HTTP_400_BAD_REQUEST
