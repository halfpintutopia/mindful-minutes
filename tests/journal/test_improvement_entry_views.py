import json
from datetime import date
# https://dennisokeeffe.medium.com/mocking-python-datetime-in-tests-with-freezegun-f5532307d6d6
from freezegun import freeze_time

from django.urls import reverse

from rest_framework import status

import pytest

from journal.models import ImprovementEntry


@pytest.mark.django_db
def test_get_list_of_improvement_entries(authenticated_user, add_improvement_entry):
    """
    GIVEN a Django application
    WHEN a user requests a list of all improvement entries
    THEN the user should receive a list of all improvement entries
    """
    client, user = authenticated_user

    improvements = [
        'Learn to be more time conscious.',
        'Plan tasks, use tools such as Pomodoro to create smaller tasks.',
        'Meditate for longer each day',
        'Take more care with my teeth.',
        'Drink more water',
    ]

    for improvement in improvements:
        add_improvement_entry(
            user=user,
            content=improvement
        )

    url = reverse(
        "improvement-entry-list-all",
        args=[user.slug]
    )

    res = client.get(
        url
    )

    assert res.status_code == status.HTTP_200_OK


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

    url = reverse(
        "improvement-entry-list-date",
        args=[user.slug, current_date]
    )

    res = client.post(
        url,
        json.dumps(improvement_data),
        content_type="application/json"
    )

    assert res.status_code == status.HTTP_201_CREATED
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

    url = reverse(
        "improvement-entry-list-date",
        args=[user.slug, current_date]
    )

    res = client.post(
        url,
        json.dumps(test_data["payload"]),
        content_type="application/json"
    )
    assert res.status_code == status.HTTP_400_BAD_REQUEST

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

    url = reverse(
        "improvement-entry-list-date",
        args=[user.slug, date_param]
    )

    res = client.post(
        url,
        improvement_data,
        content_type="application/json"
    )

    assert res.status_code == status.HTTP_403_FORBIDDEN

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

    improvement_entry = add_improvement_entry(
        content="I need to listen more and talk less.",
        user=user,
    )

    url = reverse(
        "improvement-entry-detail-single",
        args=[user.slug, current_date, improvement_entry.id]
    )

    res = client.get(
        url,
        content_type="application/json"
    )

    assert res.status_code == status.HTTP_200_OK
    assert res.data["user"] == user.id
    assert res.data["content"] == "I need to listen more and talk less."


@pytest.mark.django_db
def test_get_single_improvement_entry_incorrect_id(
    authenticated_user,
):
    """
    GIVEN a Django application
    WHEN the user requests to retrieve an improvement entry with an incorrect id
    THEN check the improvement entry is not retrieved
    """
    client, user = authenticated_user

    current_date = date.today()
    invalid_id = 14258

    url = reverse(
        "improvement-entry-detail-single",
        args=[user.slug, current_date, invalid_id]
    )

    res = client.get(url)

    assert res.status_code == status.HTTP_404_NOT_FOUND


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

    url = reverse(
        "improvement-entry-list-date",
        args=[user.slug, current_date]
    )

    res = client.get(url)

    assert res.status_code == status.HTTP_200_OK
    assert res.data[0]["created_on"] == str(current_date)

    improvement_entries = ImprovementEntry.objects.filter(
        created_on__date=current_date)
    assert len(improvement_entries) == 1


@pytest.mark.django_db
@pytest.mark.parametrize("created_on_timestamp", [
    "2023-07-06 12:00:00",
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
    date_and_time = created_on_timestamp.split(" ")
    client, user = authenticated_user

    with freeze_time(created_on_timestamp):
        improvement_entries = ImprovementEntry.objects.all()
        assert len(improvement_entries) == 0

        add_improvement_entry(
            content="I need to listen more and talk less.",
            user=user,
        )

    url = reverse(
        "improvement-entry-list-date",
        args=[user.slug, date_and_time[0]]
    )
    res = client.get(url)

    assert res.status_code == status.HTTP_200_OK
    assert res.data[0]["created_on"] == date_and_time[0]

    improvement_entries = ImprovementEntry.objects.filter(
        created_on__date=date_and_time[0])
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

    client, user = authenticated_user

    improvement_entry = add_improvement_entry(
        content="I need to listen more and talk less.",
        user=user,
    )

    improvement_date = improvement_entry.created_on.strftime("%Y-%m-%d")

    url = reverse(
        "improvement-entry-detail-single",
        args=[user.slug, improvement_date, improvement_entry.id]
    )

    res = client.get(
        url,
        content_type="application/json"
    )

    assert res.status_code == status.HTTP_200_OK
    assert res.data["content"] == "I need to listen more and talk less."

    res_delete = client.delete(
        url,
        content_type="application/json"
    )

    assert res_delete.status_code == status.HTTP_204_NO_CONTENT

    url_retrieve = reverse(
        "improvement-entry-list-date",
        args=[user.slug, improvement_date]
    )

    res_retrieve = client.get(
        url_retrieve,
        content_type="application/json"
    )

    assert res_retrieve.status_code == status.HTTP_200_OK
    assert len(res_retrieve.data) == 0

    assert not ImprovementEntry.objects.filter(
        id=improvement_entry.id).exists()

    improvement_entries = ImprovementEntry.objects.all()
    assert len(improvement_entries) == 0


@pytest.mark.django_db
def test_remove_improvement_invalid_id(
    authenticated_user
):
    """
    GIVEN a Django application
    WHEN the user requests to remove an improvement entry with an invalid id
    THEN the improvement entry is not removed
    """
    improvement_entries = ImprovementEntry.objects.all()
    assert len(improvement_entries) == 0

    current_date = date.today()
    invalid_id = 12756

    client, user = authenticated_user

    url = reverse(
        "improvement-entry-detail-single",
        args=[user.slug, current_date, invalid_id]
    )

    res = client.delete(
        url,
        content_type="application/json"
    )

    assert res.status_code == status.HTTP_404_NOT_FOUND

    updated_improvement_entries = ImprovementEntry.objects.all()
    assert len(improvement_entries) == len(updated_improvement_entries)
    assert len(updated_improvement_entries) == 0


@pytest.mark.django_db
@pytest.mark.parametrize("requested_date", [
    "2024-07-06 12:00:00",
    "2023-03-05 15:30:00",
    "2022-09-16 23:15:00"
])
def test_remove_improvement_not_current_date(
    authenticated_user, requested_date, add_improvement_entry
):
    """
    GIVEN a Django application
    WHEN the user requests to remove an improvement entry when the date is not today
    THEN the improvement entry is not removed
    """
    improvement_entries = ImprovementEntry.objects.all()
    assert len(improvement_entries) == 0

    client, user = authenticated_user
    date_and_time = requested_date.split(" ")
    current_date = date.today()

    with freeze_time(requested_date):
        improvement_entry = add_improvement_entry(
            content="I need to listen more and talk less.",
            user=user,
        )

    url = reverse(
        "improvement-entry-detail-single",
        args=[user.slug, date_and_time[0], improvement_entry.id]
    )

    res = client.delete(
        url,
        content_type="application/json"
    )

    assert res.status_code == status.HTTP_403_FORBIDDEN

    updated_improvement_entries = ImprovementEntry.objects.all()
    assert len(updated_improvement_entries) == 1


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

    url = reverse(
        "improvement-entry-detail-single",
        args=[user.slug, current_date, improvement_entry.id]
    )

    res = client.put(
        url,
        json.dumps(test_data["payload"]),
        content_type="application/json"
    )

    assert res.status_code == status.HTTP_200_OK
    assert res.data["content"] == test_data["payload"]["content"]

    res_check = client.get(
        url,
        content_type="application/json"
    )

    assert res_check.status_code == status.HTTP_200_OK
    assert res.data["content"] == test_data["payload"]["content"]

    improvement_entries = ImprovementEntry.objects.all()
    assert len(improvement_entries) == 1


@pytest.mark.django_db
def test_update_improvement_entry_incorrect_data(
    authenticated_user,
    add_improvement_entry
):
    """
    GIVEN a Django application
    WHEN the user requests to update an improvement entry with an incorrect id
    THEN the improvement entry is not updated
    """
    client, user = authenticated_user

    current_date = date.today()
    invalid_id = 12574

    add_improvement_entry(
        content="I need to listen more and talk less.",
        user=user,
    )

    improvement_data = {
        "content": "I need to be less distracted while meditating.",
        "user": user.id,
    }

    url = reverse(
        "improvement-entry-detail-single",
        args=[user.slug, current_date, invalid_id]
    )

    res = client.put(
        url,
        json.dumps(improvement_data),
        content_type="application/json"
    )

    assert res.status_code == status.HTTP_404_NOT_FOUND


@pytest.mark.django_db
@pytest.mark.parametrize("requested_date", [
    "2024-07-01 12:00:00",
    "2023-03-05 06:00:00",
    "2022-09-16 21:15:00"
])
def test_update_improvement_entry_incorrect_date(
    authenticated_user,
    requested_date,
    add_improvement_entry
):
    """
    GIVEN a Django application
    WHEN the user requests to update an improvement entry with an incorrect date
    THEN the improvement entry is not and permission denied
    """
    date_and_time = requested_date.split(" ")

    client, user = authenticated_user

    with freeze_time(requested_date):
        improvement_entry = add_improvement_entry(
            content="I need to listen more and talk less.",
            user=user,
        )

    url = reverse(
        "improvement-entry-detail-single",
        args=[user.slug, date_and_time[0], improvement_entry.id]
    )

    res = client.put(
        url,
        content_type="application/json"
    )

    assert res.status_code == status.HTTP_403_FORBIDDEN


@pytest.mark.django_db
@pytest.mark.parametrize("test_data", [
    {
        "payload": {},
    },
    {
        "payload": {
            "content entry": "I need to listen more and talk less.",
        },
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

    url = reverse(
        "improvement-entry-detail-single",
        args=[user.slug, current_date, improvement_entry.id]
    )

    res = client.put(
        url,
        test_data["payload"],
        content_type="application/json"
    )

    assert res.status_code == status.HTTP_400_BAD_REQUEST
