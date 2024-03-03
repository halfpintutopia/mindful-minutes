import json
from datetime import date

import pytest
from django.urls import reverse
from freezegun import freeze_time
from rest_framework import status

from knowledge_entries.models import KnowledgeEntry


@pytest.mark.django_db
def test_get_list_of_knowledge_entries(authenticated_user, add_knowledge_entry):
    """
    GIVEN a Django application
    WHEN a user requests a list of all knowledge entries
    THEN the user should receive a list of all knowledge entries
    """
    client, user = authenticated_user

    knowledge_entries = [
        "Was able to explain specificity to a colleague.",
        "Finished the course on Docker.",
        "Wrote a blog entry to share knowledge regarding how to write an "
        "README.",
        "Finished video on Django.",
    ]

    for knowledge in knowledge_entries:
        add_knowledge_entry(user=user, content=knowledge)

    url = reverse("knowledge-entry-list", args=[user.slug])

    res = client.get(url)

    assert res.status_code == status.HTTP_200_OK


@pytest.mark.django_db
def test_add_knowledge_entry(authenticated_user):
    """
    GIVEN a Django application
    WHEN the user requests to add knowledge entry
    THEN check that the knowledge entry is added
    """
    knowledge_entries = KnowledgeEntry.objects.all()
    assert len(knowledge_entries) == 0

    current_date = date.today()

    client, user = authenticated_user

    knowledge_data = {
        "content": "Understand the problem with my function. Was able to "
        "understand 75% of this.",
        "user": user.id,
    }

    url = reverse("knowledge-entry-date-list", args=[user.slug, current_date])

    res = client.post(
        url, json.dumps(knowledge_data), content_type="application/json"
    )

    assert res.status_code == status.HTTP_201_CREATED
    assert res.data["user"] == user.id
    assert (
        res.data["content"] == "Understand the problem with my function. Was "
        "able to understand 75% of this."
    )

    knowledge_entries = KnowledgeEntry.objects.all()
    assert len(knowledge_entries) == 1


@pytest.mark.django_db
@pytest.mark.parametrize(
    "test_data",
    [
        {"payload": {}, "status_code": 400},
        {
            "payload": {
                "content entry": "Understand the problem with my function. "
                "Was able to understand 75% of this.",
            },
            "status_code": 400,
        },
    ],
)
def test_add_knowledge_entry_incorrect_json(authenticated_user, test_data):
    """
    GIVEN a Django application
    WHEN the user requests to add knowledge entry with an invalid payload
    THEN the payload is not sent
    """
    knowledge_entries = KnowledgeEntry.objects.all()
    assert len(knowledge_entries) == 0

    current_date = date.today()

    client, user = authenticated_user

    test_data["payload"]["user"] = user.id

    url = reverse("knowledge-entry-date-list", args=[user.slug, current_date])

    res = client.post(
        url, json.dumps(test_data["payload"]), content_type="application/json"
    )
    assert res.status_code == status.HTTP_400_BAD_REQUEST

    knowledge_entries = KnowledgeEntry.objects.all()
    assert len(knowledge_entries) == 0


@pytest.mark.django_db
@pytest.mark.parametrize("date_param", ["2023-07-01", "2023-06-20"])
def test_add_knowledge_entry_not_current_date(authenticated_user, date_param):
    """
    GIVEN a Django application
    WHEN the user attempts to add knowledge entry on a date,
    that is not the current date
    THEN the knowledge entry is not created
    """
    knowledge_entries = KnowledgeEntry.objects.all()
    assert len(knowledge_entries) == 0

    client, user = authenticated_user

    knowledge_data = {
        "content": "Understand the problem with my function. Was able to "
        "understand 75% of this.",
        "user": user.id,
    }

    url = reverse("knowledge-entry-date-list", args=[user.slug, date_param])

    res = client.post(url, knowledge_data, content_type="application/json")

    assert res.status_code == status.HTTP_403_FORBIDDEN

    knowledge_entries = KnowledgeEntry.objects.all()
    assert len(knowledge_entries) == 0


@pytest.mark.django_db
def test_get_single_knowledge_entry(authenticated_user, add_knowledge_entry):
    """
    GIVEN a Django application
    WHEN the user requests to retrieve knowledge entry
    THEN check that the knowledge entry is retrieved
    """
    current_date = date.today()

    client, user = authenticated_user

    knowledge_entry = add_knowledge_entry(
        content="Understand the problem with my function. Was able to "
        "understand 75% of this.",
        user=user,
    )

    url = reverse(
        "knowledge-entry-detail",
        args=[user.slug, current_date, knowledge_entry.id],
    )

    res = client.get(url, content_type="application/json")

    assert res.status_code == status.HTTP_200_OK
    assert res.data["user"] == user.id
    assert (
        res.data["content"] == "Understand the problem with my function. Was "
        "able to understand 75% of this."
    )


@pytest.mark.django_db
def test_get_single_knowledge_entry_incorrect_id(
    authenticated_user,
):
    """
    GIVEN a Django application
    WHEN the user requests to retrieve an knowledge entry with an incorrect id
    THEN check the knowledge entry is not retrieved
    """
    client, user = authenticated_user

    current_date = date.today()
    invalid_id = 14258

    url = reverse(
        "knowledge-entry-detail",
        args=[user.slug, current_date, invalid_id],
    )

    res = client.get(url)

    assert res.status_code == status.HTTP_404_NOT_FOUND


@pytest.mark.django_db
def test_get_all_knowledge_entries_by_current_date(
    authenticated_user, add_knowledge_entry
):
    """
    GIVEN a Django application
    WHEN the user requests to retrieve all knowledge entries
    by current date
    THEN check all knowledge entries are retrieved
    """
    knowledge_entries = KnowledgeEntry.objects.all()
    assert len(knowledge_entries) == 0

    current_date = date.today()

    client, user = authenticated_user

    add_knowledge_entry(
        content="Understand the problem with my function. Was able to "
        "understand 75% of this.",
        user=user,
    )

    url = reverse("knowledge-entry-date-list", args=[user.slug, current_date])

    res = client.get(url)

    assert res.status_code == status.HTTP_200_OK
    assert res.data[0]["created_on"] == str(current_date)

    knowledge_entries = KnowledgeEntry.objects.filter(
        created_on__date=current_date
    )
    assert len(knowledge_entries) == 1


@pytest.mark.django_db
@pytest.mark.parametrize(
    "created_on_timestamp",
    [
        "2023-07-06 12:00:00",
        "2023-06-04 10:30:00",
        "2022-07-09 19:45:00",
    ],
)
def test_get_all_knowledge_entries_by_date(
    authenticated_user, add_knowledge_entry, created_on_timestamp
):
    """
    GIVEN a Django application
    WHEN the user requests to retrieve all knowledge entries by date
    THEN check all knowledge entries are retrieved
    """
    date_and_time = created_on_timestamp.split(" ")
    client, user = authenticated_user

    with freeze_time(created_on_timestamp):
        knowledge_entries = KnowledgeEntry.objects.all()
        assert len(knowledge_entries) == 0

        add_knowledge_entry(
            content="Understand the problem with my function. Was able to "
            "understand 75% of this.",
            user=user,
        )

    url = reverse(
        "knowledge-entry-date-list", args=[user.slug, date_and_time[0]]
    )
    res = client.get(url)

    assert res.status_code == status.HTTP_200_OK
    assert res.data[0]["created_on"] == date_and_time[0]

    knowledge_entries = KnowledgeEntry.objects.filter(
        created_on__date=date_and_time[0]
    )
    assert len(knowledge_entries) == 1


@pytest.mark.django_db
def test_remove_knowledge_entry(authenticated_user, add_knowledge_entry):
    """
    GIVEN a Django application
    WHEN the user requests to remove knowledge entry
    THEN the knowledge entry is removed
    """
    knowledge_entries = KnowledgeEntry.objects.all()
    assert len(knowledge_entries) == 0

    client, user = authenticated_user

    knowledge_entry = add_knowledge_entry(
        content="Understand the problem with my function. Was able to "
        "understand 75% of this.",
        user=user,
    )

    knowledge_date = knowledge_entry.created_on.strftime("%Y-%m-%d")

    url = reverse(
        "knowledge-entry-detail",
        args=[user.slug, knowledge_date, knowledge_entry.id],
    )

    res = client.get(url, content_type="application/json")

    assert res.status_code == status.HTTP_200_OK
    assert (
        res.data["content"] == "Understand the problem with my function. Was "
        "able to understand 75% of this."
    )

    res_delete = client.delete(url, content_type="application/json")

    assert res_delete.status_code == status.HTTP_204_NO_CONTENT

    url_retrieve = reverse(
        "knowledge-entry-date-list", args=[user.slug, knowledge_date]
    )

    res_retrieve = client.get(url_retrieve, content_type="application/json")

    assert res_retrieve.status_code == status.HTTP_200_OK
    assert len(res_retrieve.data) == 0

    assert not KnowledgeEntry.objects.filter(id=knowledge_entry.id).exists()

    knowledge_entries = KnowledgeEntry.objects.all()
    assert len(knowledge_entries) == 0


@pytest.mark.django_db
def test_remove_knowledge_invalid_id(authenticated_user):
    """
    GIVEN a Django application
    WHEN the user requests to remove knowledge entry with an invalid id
    THEN the knowledge entry is not removed
    """
    knowledge_entries = KnowledgeEntry.objects.all()
    assert len(knowledge_entries) == 0

    current_date = date.today()
    invalid_id = 12756

    client, user = authenticated_user

    url = reverse(
        "knowledge-entry-detail",
        args=[user.slug, current_date, invalid_id],
    )

    res = client.delete(url, content_type="application/json")

    assert res.status_code == status.HTTP_404_NOT_FOUND

    updated_knowledge_entries = KnowledgeEntry.objects.all()
    assert len(knowledge_entries) == len(updated_knowledge_entries)
    assert len(updated_knowledge_entries) == 0


@pytest.mark.django_db
@pytest.mark.parametrize(
    "requested_date",
    ["2024-07-06 12:00:00", "2023-03-05 15:30:00", "2022-09-16 23:15:00"],
)
def test_remove_knowledge_not_current_date(
    authenticated_user, requested_date, add_knowledge_entry
):
    """
    GIVEN a Django application
    WHEN the user requests to remove knowledge entry when the date is not
    today
    THEN the knowledge entry is not removed
    """
    knowledge_entries = KnowledgeEntry.objects.all()
    assert len(knowledge_entries) == 0

    client, user = authenticated_user
    date_and_time = requested_date.split(" ")

    with freeze_time(requested_date):
        knowledge_entry = add_knowledge_entry(
            content="Understand the problem with my function. Was able to "
            "understand 75% of this.",
            user=user,
        )

    url = reverse(
        "knowledge-entry-detail",
        args=[user.slug, date_and_time[0], knowledge_entry.id],
    )

    res = client.delete(url, content_type="application/json")

    assert res.status_code == status.HTTP_403_FORBIDDEN

    updated_knowledge_entries = KnowledgeEntry.objects.all()
    assert len(updated_knowledge_entries) == 1


@pytest.mark.django_db
@pytest.mark.parametrize(
    "test_data",
    [
        {
            "payload": {
                "content": "Understand the problem with my function. Was "
                "able "
                "to understand 75% of this. Refactored code with "
                "new knowledge.",
            }
        },
        {
            "payload": {
                "content": "Read a chapter of Eloquent JavaScript and was "
                "able to explain this to another colleague.",
            }
        },
    ],
)
def test_update_knowledge_entry(
    authenticated_user, add_knowledge_entry, test_data
):
    """
    GIVEN a Django application
    WHEN the user requests to update knowledge entry
    THEN the knowledge entry is updated
    """
    knowledge_entries = KnowledgeEntry.objects.all()
    assert len(knowledge_entries) == 0

    current_date = date.today()

    client, user = authenticated_user

    knowledge_entry = add_knowledge_entry(
        content="Understand the problem with my function. Was able to "
        "understand 75% of this.",
        user=user,
    )

    test_data["payload"]["user"] = user.id

    url = reverse(
        "knowledge-entry-detail",
        args=[user.slug, current_date, knowledge_entry.id],
    )

    res = client.put(
        url, json.dumps(test_data["payload"]), content_type="application/json"
    )

    assert res.status_code == status.HTTP_200_OK
    assert res.data["content"] == test_data["payload"]["content"]

    res_check = client.get(url, content_type="application/json")

    assert res_check.status_code == status.HTTP_200_OK
    assert res.data["content"] == test_data["payload"]["content"]

    knowledge_entries = KnowledgeEntry.objects.all()
    assert len(knowledge_entries) == 1


@pytest.mark.django_db
def test_update_knowledge_entry_incorrect_data(
    authenticated_user, add_knowledge_entry
):
    """
    GIVEN a Django application
    WHEN the user requests to update knowledge entry with an incorrect id
    THEN the knowledge entry is not updated
    """
    client, user = authenticated_user

    current_date = date.today()
    invalid_id = 12574

    add_knowledge_entry(
        content="Understand the problem with my function. Was able to "
        "understand 75% of this.",
        user=user,
    )

    knowledge_data = {
        "content": "Read a chapter of Eloquent JavaScript and was able to "
        "explain this to another colleague.",
        "user": user.id,
    }

    url = reverse(
        "knowledge-entry-detail",
        args=[user.slug, current_date, invalid_id],
    )

    res = client.put(
        url, json.dumps(knowledge_data), content_type="application/json"
    )

    assert res.status_code == status.HTTP_404_NOT_FOUND


@pytest.mark.django_db
@pytest.mark.parametrize(
    "requested_date",
    ["2024-07-01 12:00:00", "2023-03-05 06:00:00", "2022-09-16 21:15:00"],
)
def test_update_knowledge_entry_incorrect_date(
    authenticated_user, requested_date, add_knowledge_entry
):
    """
    GIVEN a Django application
    WHEN the user requests to update knowledge entry with an incorrect date
    THEN the knowledge entry is not and permission denied
    """
    date_and_time = requested_date.split(" ")

    client, user = authenticated_user

    with freeze_time(requested_date):
        knowledge_entry = add_knowledge_entry(
            content="Understand the problem with my function. Was able to "
            "understand 75% of this.",
            user=user,
        )

    url = reverse(
        "knowledge-entry-detail",
        args=[user.slug, date_and_time[0], knowledge_entry.id],
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
                "content entry": "Understand the problem with my function. "
                "Was able to understand 75% of this.",
            },
        },
    ],
)
def test_update_knowledge_entry_invalid_json(
    authenticated_user, add_knowledge_entry, test_data
):
    """
    GIVEN a Django application
    WHEN the user requests to update knowledge entry with invalid JSON
    THEN the knowledge entry is not updated
    """
    client, user = authenticated_user

    current_date = date.today()

    knowledge_entry = add_knowledge_entry(
        content="Dentist",
        user=user,
    )

    url = reverse(
        "knowledge-entry-detail",
        args=[user.slug, current_date, knowledge_entry.id],
    )

    res = client.put(url, test_data["payload"], content_type="application/json")

    assert res.status_code == status.HTTP_400_BAD_REQUEST
