from datetime import date
# https://dennisokeeffe.medium.com/mocking-python-datetime-in-tests-with-freezegun-f5532307d6d6
from freezegun import freeze_time

import pytest

from journal.models import KnowledgeEntry


@pytest.mark.django_db
def test_add_knowledge_entry(authenticated_user):
    """
    GIVEN a Django application
    WHEN the user requests to add an knowledge entry
    THEN check that the knowledge entry is added
    """
    knowledge_entries = KnowledgeEntry.objects.all()
    assert len(knowledge_entries) == 0

    current_date = date.today()

    client, user = authenticated_user

    knowledge_data = {
        "content": "Understand the problem with my function. Was able to understand 75% of this.",
        "user": user.id,
    }

    res = client.post(
        f"/api/knowledge/{current_date}/",
        knowledge_data,
        format="json"
    )

    print("Response data", res.data)

    assert res.status_code == 201
    assert res.data["user"] == user.id
    assert res.data["content"] == "Understand the problem with my function. Was able to understand 75% of this."

    knowledge_entries = KnowledgeEntry.objects.all()
    assert len(knowledge_entries) == 1


@pytest.mark.django_db
@pytest.mark.parametrize("test_data", [
    {
        "payload": {},
        "status_code": 400
    },
    {
        "payload": {
            "content entry": "Understand the problem with my function. Was able to understand 75% of this.",
        },
        "status_code": 400
    }
])
def test_add_knowledge_entry_incorrect_json(authenticated_user, test_data):
    """
    GIVEN a Django application
    WHEN the user requests to add an knowledge entry with an invalid payload
    THEN the payload is not sent
    """
    knowledge_entries = KnowledgeEntry.objects.all()
    assert len(knowledge_entries) == 0

    current_date = date.today()

    client, user = authenticated_user

    test_data["payload"]["user"] = user.id

    res = client.post(
        f"/api/knowledge/{current_date}/",
        test_data["payload"],
        format="json"
    )
    assert res.status_code == 400

    knowledge_entries = KnowledgeEntry.objects.all()
    assert len(knowledge_entries) == 0


@pytest.mark.django_db
@pytest.mark.parametrize("date_param", ["2023-07-01", "2023-06-20"])
def test_add_knowledge_entry_not_current_date(
    authenticated_user,
    date_param
):
    """
    GIVEN a Django application
    WHEN the user attempts to add an knowledge entry on a date,
    that is not the current date
    THEN the knowledge entry is not created
    """
    knowledge_entries = KnowledgeEntry.objects.all()
    assert len(knowledge_entries) == 0

    client, user = authenticated_user

    knowledge_data = {
        "content": "Understand the problem with my function. Was able to understand 75% of this.",
        "user": user.id,
    }

    res = client.post(
        f"/api/knowledge/{date_param}/",
        knowledge_data,
        format="json"
    )

    assert res.status_code == 403

    knowledge_entries = KnowledgeEntry.objects.all()
    assert len(knowledge_entries) == 0


@pytest.mark.django_db
def test_get_single_knowledge_entry(
    authenticated_user,
    add_knowledge_entry
):
    """
    GIVEN a Django application
    WHEN the user requests to retrieve an knowledge entry
    THEN check that the knowledge entry is retrieved
    """
    current_date = date.today()

    client, user = authenticated_user

    knowledge = add_knowledge_entry(
        content="Understand the problem with my function. Was able to understand 75% of this.",
        user=user,
    )

    res = client.get(
        f"/api/knowledge/{current_date}/{knowledge.id}/",
        format="json"
    )

    assert res.status_code == 200
    assert res.data["user"] == user.id
    assert res.data["content"] == "Understand the problem with my function. Was able to understand 75% of this."


@pytest.mark.django_db
@pytest.mark.parametrize("invalid_id", ["random", "1", 14258])
def test_get_single_knowledge_entry_incorrect_id(
    authenticated_user,
    invalid_id
):
    """
    GIVEN a Django application
    WHEN the user requests to retrieve an knowledge entry with an incorrect id
    THEN check the knowledge entry is not retrieved
    """
    (client, *_) = authenticated_user

    current_date = date.today()

    res = client.get(f"/api/knowledge/{current_date}/{invalid_id}/")

    assert res.status_code == 404


@pytest.mark.django_db
def test_get_all_knowledge_entries_by_current_date(
    authenticated_user,
    add_knowledge_entry
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
        content="Understand the problem with my function. Was able to understand 75% of this.",
        user=user,
    )

    res = client.get(f"/api/knowledge/{str(current_date)}/")

    assert res.status_code == 200
    assert res.data[0]["created_on"] == str(current_date)

    knowledge_entries = KnowledgeEntry.objects.filter(
        created_on__date=current_date)
    assert len(knowledge_entries) == 1


@pytest.mark.django_db
@pytest.mark.parametrize("created_on_timestamp", [
    "2023-04-06 12:00:00",
    "2023-06-04 10:30:00",
    "2022-07-09 19:45:00",
])
def test_get_all_knowledge_entries_by_date(
    authenticated_user,
    add_knowledge_entry,
    created_on_timestamp
):
    """
    GIVEN a Django application
    WHEN the user requests to retrieve all knowledge entries by date
    THEN check all knowledge entries are retrieved
    """
    with freeze_time(created_on_timestamp):
        knowledge_entries = KnowledgeEntry.objects.all()
        assert len(knowledge_entries) == 0

        current_date = date.today()

        client, user = authenticated_user

        add_knowledge_entry(
            content="Understand the problem with my function. Was able to understand 75% of this.",
            user=user,
        )

        res = client.get(f"/api/knowledge/{str(current_date)}/")

        assert res.status_code == 200
        assert res.data[0]["created_on"] == str(current_date)

        knowledge_entries = KnowledgeEntry.objects.filter(
            created_on__date=current_date)
        assert len(knowledge_entries) == 1


@pytest.mark.django_db
def test_remove_knowledge_entry(
    authenticated_user,
    add_knowledge_entry
):
    """
    GIVEN a Django application
    WHEN the user requests to remove an knowledge entry
    THEN the knowledge entry is removed
    """
    knowledge_entries = KnowledgeEntry.objects.all()
    assert len(knowledge_entries) == 0

    current_date = date.today()

    client, user = authenticated_user

    knowledge_entry = add_knowledge_entry(
        content="Understand the problem with my function. Was able to understand 75% of this.",
        user=user,
    )

    res = client.get(
        f"/api/knowledge/{current_date}/{knowledge_entry.id}/",
        format="json"
    )

    assert res.status_code == 200
    assert res.data["content"] == "Understand the problem with my function. Was able to understand 75% of this."

    res_delete = client.delete(
        f"/api/knowledge/{current_date}/{knowledge_entry.id}/",
        format="json"
    )

    assert res_delete.status_code == 204

    res_retrieve = client.get(
        f"/api/knowledge/{current_date}/", format="json")

    assert res_retrieve.status_code == 200
    assert len(res_retrieve.data) == 0

    assert not KnowledgeEntry.objects.filter(id=knowledge_entry.id).exists()

    knowledge_entries = KnowledgeEntry.objects.all()
    assert len(knowledge_entries) == 0


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
def test_remove_knowledge_invalid_id(
    authenticated_user,
    test_data
):
    """
    GIVEN a Django application
    WHEN the user requests to remove an knowledge entry with an invalid id
    THEN the knowledge entry is not removed
    """
    knowledge_entries = KnowledgeEntry.objects.all()
    assert len(knowledge_entries) == 0

    current_date = date.today()

    (client, *_) = authenticated_user

    res = client.delete(
        f"/api/knowledge/{current_date}/{test_data['incorrect_id']}/",
        format="json"
    )

    assert res.status_code == test_data["expected_status_code"]

    updated_knowledge_entries = KnowledgeEntry.objects.all()
    assert len(knowledge_entries) == len(updated_knowledge_entries)
    assert len(updated_knowledge_entries) == 0


@pytest.mark.django_db
@pytest.mark.parametrize("requested_date", [
    "2024-07-06", "2023-03-05", "2022-09-16"
])
def test_remove_knowledge_not_current_date(
    authenticated_user, requested_date
):
    """
    GIVEN a Django application
    WHEN the user requests to remove an knowledge entry when the date is not today
    THEN the knowledge entry is not removed
    """
    knowledge_entries = KnowledgeEntry.objects.all()
    assert len(knowledge_entries) == 0

    (client, *_) = authenticated_user

    res = client.delete(
        f"/api/knowledge/{requested_date}/1/", format="json")

    assert res.status_code == 403

    updated_knowledge_entries = KnowledgeEntry.objects.all()
    assert len(knowledge_entries) == len(updated_knowledge_entries)
    assert len(updated_knowledge_entries) == 0


@pytest.mark.django_db
@pytest.mark.parametrize("test_data", [
    {
        "payload": {
            "content": "Understand the problem with my function. Was able to understand 75% of this. Refactored code with new knowledge",
        }
    },
    {
        "payload": {
            "content": "Read a chapter of Eloquent JavaScript and was able to explain this to another colleague",
        }
    }
])
def test_update_knowledge_entry(
    authenticated_user,
    add_knowledge_entry,
    test_data
):
    """
    GIVEN a Django application
    WHEN the user requests to update an knowledge entry
    THEN the knowledge entry is updated
    """
    knowledge_entries = KnowledgeEntry.objects.all()
    assert len(knowledge_entries) == 0

    current_date = date.today()

    client, user = authenticated_user

    knowledge_entry = add_knowledge_entry(
        content="Understand the problem with my function. Was able to understand 75% of this.",
        user=user,
    )

    test_data["payload"]["user"] = user.id

    res = client.put(
        f"/api/knowledge/{current_date}/{knowledge_entry.id}/",
        test_data["payload"],
        format="json"
    )

    assert res.status_code == 200
    assert res.data["content"] == test_data["payload"]["content"]

    res_check = client.get(
        f"/api/knowledge/{current_date}/{knowledge_entry.id}/",
        format="json"
    )

    assert res_check.status_code == 200
    assert res.data["content"] == test_data["payload"]["content"]

    knowledge_entries = KnowledgeEntry.objects.all()
    assert len(knowledge_entries) == 1


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
def test_update_knowledge_entry_incorrect_data(
    authenticated_user,
    add_knowledge_entry,
    test_data
):
    """
    GIVEN a Django application
    WHEN the user requests to update an knowledge entry with an incorrect id
    THEN the knowledge entry is not updated
    """
    client, user = authenticated_user

    current_date = date.today()

    add_knowledge_entry(
        content="Understand the problem with my function. Was able to understand 75% of this.",
        user=user,
    )

    knowledge_data = {
        "content": "Read a chapter of Eloquent JavaScript and was able to explain this to another colleague",
        "user": user.id,
    }

    res = client.put(
        f"/api/knowledge/{current_date}/{test_data['incorrect_id']}/",
        knowledge_data,
        format="json"
    )

    print("response data", res)

    assert res.status_code == test_data["expected_status_code"]


@pytest.mark.django_db
@pytest.mark.parametrize("requested_date", [
    "2024-07-06", "2023-03-05", "2022-09-16"
])
def test_update_knowledge_entry_incorrect_date(
    authenticated_user,
    requested_date
):
    """
    GIVEN a Django application
    WHEN the user requests to update an knowledge entry with an incorrect date
    THEN the knowledge entry is not and permission denied
    """
    (client, *_) = authenticated_user

    res = client.put(
        f"/api/knowledge/{requested_date}/1/",
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
            "content entry": "Understand the problem with my function. Was able to understand 75% of this.",
        },
        "expected_status_code": 400
    }
])
def test_update_knowledge_entry_invalid_json(
    authenticated_user,
    add_knowledge_entry,
    test_data
):
    """
    GIVEN a Django application
    WHEN the user requests to update an knowledge entry with invalid JSON
    THEN the knowledge entry is not updated
    """
    client, user = authenticated_user

    current_date = date.today()

    knowledge_entry = add_knowledge_entry(
        content="Dentist",
        user=user,
    )

    res = client.put(
        f"/api/knowledge/{current_date}/{knowledge_entry.id}/",
        test_data["payload"],
        format="json"
    )

    assert res.status_code == test_data["expected_status_code"]
