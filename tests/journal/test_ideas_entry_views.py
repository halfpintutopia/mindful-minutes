from datetime import date
# https://dennisokeeffe.medium.com/mocking-python-datetime-in-tests-with-freezegun-f5532307d6d6
from freezegun import freeze_time

import pytest

from journal.models import IdeasEntry


@pytest.mark.django_db
def test_add_ideas_entry(authenticated_user):
    """
    GIVEN a Django application
    WHEN the user requests to add an ideas entry
    THEN check that the ideas entry is added
    """
    ideas_entries = IdeasEntry.objects.all()
    assert len(ideas_entries) == 0

    current_date = date.today()

    client, user = authenticated_user

    ideas_data = {
        "content": "I am healthy. My studies are going well. I am free and strong.",
        "user": user.id,
    }

    res = client.post(
        f"/api/ideas/{current_date}/",
        ideas_data,
        format="json"
    )

    print("Response data", res.data)

    assert res.status_code == 201
    assert res.data["user"] == user.id
    assert res.data["content"] == "I am healthy. My studies are going well. I am free and strong."

    ideas_entries = IdeasEntry.objects.all()
    assert len(ideas_entries) == 1


@pytest.mark.django_db
@pytest.mark.parametrize("test_data", [
    {
        "payload": {},
        "status_code": 400
    },
    {
        "payload": {
            "content entry": "I am healthy. My studies are going well. I am free and strong.",
        },
        "status_code": 400
    }
])
def test_add_ideas_entry_incorrect_json(authenticated_user, test_data):
    """
    GIVEN a Django application
    WHEN the user requests to add an ideas entry with an invalid payload
    THEN the payload is not sent
    """
    ideas_entries = IdeasEntry.objects.all()
    assert len(ideas_entries) == 0

    current_date = date.today()

    client, user = authenticated_user

    test_data["payload"]["user"] = user.id

    res = client.post(
        f"/api/ideas/{current_date}/",
        test_data["payload"],
        format="json"
    )
    assert res.status_code == 400

    ideas_entries = IdeasEntry.objects.all()
    assert len(ideas_entries) == 0


@pytest.mark.django_db
@pytest.mark.parametrize("date_param", ["2023-07-01", "2023-06-20"])
def test_add_ideas_entry_not_current_date(
    authenticated_user,
    date_param
):
    """
    GIVEN a Django application
    WHEN the user attempts to add an ideas entry on a date,
    that is not the current date
    THEN the ideas entry is not created
    """
    ideas_entries = IdeasEntry.objects.all()
    assert len(ideas_entries) == 0

    client, user = authenticated_user

    ideas_data = {
        "content": "I am healthy. My studies are going well. I am free and strong.",
        "user": user.id,
    }

    res = client.post(
        f"/api/ideas/{date_param}/",
        ideas_data,
        format="json"
    )

    assert res.status_code == 403

    ideas_entries = IdeasEntry.objects.all()
    assert len(ideas_entries) == 0


@pytest.mark.django_db
def test_get_single_ideas_entry(
    authenticated_user,
    add_ideas_entry
):
    """
    GIVEN a Django application
    WHEN the user requests to retrieve an ideas entry
    THEN check that the ideas entry is retrieved
    """
    current_date = date.today()

    client, user = authenticated_user

    ideas = add_ideas_entry(
        content="I am healthy. My studies are going well. I am free and strong.",
        user=user,
    )

    res = client.get(
        f"/api/ideas/{current_date}/{ideas.id}/",
        format="json"
    )

    assert res.status_code == 200
    assert res.data["user"] == user.id
    assert res.data["content"] == "I am healthy. My studies are going well. I am free and strong."


@pytest.mark.django_db
@pytest.mark.parametrize("invalid_id", ["random", "1", 14258])
def test_get_single_ideas_entry_incorrect_id(
    authenticated_user,
    invalid_id
):
    """
    GIVEN a Django application
    WHEN the user requests to retrieve an ideas entry with an incorrect id
    THEN check the ideas entry is not retrieved
    """
    (client, *_) = authenticated_user

    current_date = date.today()

    res = client.get(f"/api/ideas/{current_date}/{invalid_id}/")

    assert res.status_code == 404


@pytest.mark.django_db
def test_get_all_ideas_entries_by_current_date(
    authenticated_user,
    add_ideas_entry
):
    """
    GIVEN a Django application
    WHEN the user requests to retrieve all ideas entries
    by current date
    THEN check all ideas entries are retrieved
    """
    ideas_entries = IdeasEntry.objects.all()
    assert len(ideas_entries) == 0

    current_date = date.today()

    client, user = authenticated_user

    add_ideas_entry(
        content="I am healthy. My studies are going well. I am free and strong.",
        user=user,
    )

    res = client.get(f"/api/ideas/{str(current_date)}/")

    assert res.status_code == 200
    assert res.data[0]["created_on"] == str(current_date)

    ideas_entries = IdeasEntry.objects.filter(
        created_on__date=current_date)
    assert len(ideas_entries) == 1


@pytest.mark.django_db
@pytest.mark.parametrize("created_on_timestamp", [
    "2023-07-06 12:00:00",
    "2023-06-04 10:30:00",
    "2022-07-09 19:45:00",
])
def test_get_all_ideas_entries_by_date(
    authenticated_user,
    add_ideas_entry,
    created_on_timestamp
):
    """
    GIVEN a Django application
    WHEN the user requests to retrieve all ideas entries by date
    THEN check all ideas entries are retrieved
    """
    with freeze_time(created_on_timestamp):
        ideas_entries = IdeasEntry.objects.all()
        assert len(ideas_entries) == 0

        current_date = date.today()

        client, user = authenticated_user

        add_ideas_entry(
            content="I am healthy. My studies are going well. I am free and strong.",
            user=user,
        )

        res = client.get(f"/api/ideas/{str(current_date)}/")

        assert res.status_code == 200
        assert res.data[0]["created_on"] == str(current_date)

        ideas_entries = IdeasEntry.objects.filter(
            created_on__date=current_date)
        assert len(ideas_entries) == 1


@pytest.mark.django_db
def test_remove_ideas_entry(
    authenticated_user,
    add_ideas_entry
):
    """
    GIVEN a Django application
    WHEN the user requests to remove an ideas entry
    THEN the ideas entry is removed
    """
    ideas_entries = IdeasEntry.objects.all()
    assert len(ideas_entries) == 0

    current_date = date.today()

    client, user = authenticated_user

    ideas_entry = add_ideas_entry(
        content="I am healthy. My studies are going well. I am free and strong.",
        user=user,
    )

    res = client.get(
        f"/api/ideas/{current_date}/{ideas_entry.id}/",
        format="json"
    )

    assert res.status_code == 200
    assert res.data["content"] == "I am healthy. My studies are going well. I am free and strong."

    res_delete = client.delete(
        f"/api/ideas/{current_date}/{ideas_entry.id}/",
        format="json"
    )

    assert res_delete.status_code == 204

    res_retrieve = client.get(
        f"/api/ideas/{current_date}/", format="json")

    assert res_retrieve.status_code == 200
    assert len(res_retrieve.data) == 0

    assert not IdeasEntry.objects.filter(id=ideas_entry.id).exists()

    ideas_entries = IdeasEntry.objects.all()
    assert len(ideas_entries) == 0


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
def test_remove_ideas_invalid_id(
    authenticated_user,
    test_data
):
    """
    GIVEN a Django application
    WHEN the user requests to remove an ideas entry with an invalid id
    THEN the ideas entry is not removed
    """
    ideas_entries = IdeasEntry.objects.all()
    assert len(ideas_entries) == 0

    current_date = date.today()

    (client, *_) = authenticated_user

    res = client.delete(
        f"/api/ideas/{current_date}/{test_data['incorrect_id']}/",
        format="json"
    )

    assert res.status_code == test_data["expected_status_code"]

    updated_ideas_entries = IdeasEntry.objects.all()
    assert len(ideas_entries) == len(updated_ideas_entries)
    assert len(updated_ideas_entries) == 0


@pytest.mark.django_db
@pytest.mark.parametrize("requested_date", [
    "2023-07-06", "2023-03-05", "2022-09-16"
])
def test_remove_ideas_not_current_date(
    authenticated_user, requested_date
):
    """
    GIVEN a Django application
    WHEN the user requests to remove an ideas entry when the date is not today
    THEN the ideas entry is not removed
    """
    ideas_entries = IdeasEntry.objects.all()
    assert len(ideas_entries) == 0

    (client, *_) = authenticated_user

    res = client.delete(
        f"/api/ideas/{requested_date}/1/", format="json")

    assert res.status_code == 403

    updated_ideas_entries = IdeasEntry.objects.all()
    assert len(ideas_entries) == len(updated_ideas_entries)
    assert len(updated_ideas_entries) == 0


@pytest.mark.django_db
@pytest.mark.parametrize("test_data", [
    {
        "payload": {
            "content": "I am healthy. My studies are going well. I am free and strong. Refactored code with new ideas",
        }
    },
    {
        "payload": {
            "content": "Read a chapter of Eloquent JavaScript and was able to explain this to another colleague",
        }
    }
])
def test_update_ideas_entry(
    authenticated_user,
    add_ideas_entry,
    test_data
):
    """
    GIVEN a Django application
    WHEN the user requests to update an ideas entry
    THEN the ideas entry is updated
    """
    ideas_entries = IdeasEntry.objects.all()
    assert len(ideas_entries) == 0

    current_date = date.today()

    client, user = authenticated_user

    ideas_entry = add_ideas_entry(
        content="I am healthy. My studies are going well. I am free and strong.",
        user=user,
    )

    test_data["payload"]["user"] = user.id

    res = client.put(
        f"/api/ideas/{current_date}/{ideas_entry.id}/",
        test_data["payload"],
        format="json"
    )

    assert res.status_code == 200
    assert res.data["content"] == test_data["payload"]["content"]

    res_check = client.get(
        f"/api/ideas/{current_date}/{ideas_entry.id}/",
        format="json"
    )

    assert res_check.status_code == 200
    assert res.data["content"] == test_data["payload"]["content"]

    ideas_entries = IdeasEntry.objects.all()
    assert len(ideas_entries) == 1


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
def test_update_ideas_entry_incorrect_data(
    authenticated_user,
    add_ideas_entry,
    test_data
):
    """
    GIVEN a Django application
    WHEN the user requests to update an ideas entry with an incorrect id
    THEN the ideas entry is not updated
    """
    client, user = authenticated_user

    current_date = date.today()

    add_ideas_entry(
        content="I am healthy. My studies are going well. I am free and strong.",
        user=user,
    )

    ideas_data = {
        "content": "Read a chapter of Eloquent JavaScript and was able to explain this to another colleague",
        "user": user.id,
    }

    res = client.put(
        f"/api/ideas/{current_date}/{test_data['incorrect_id']}/",
        ideas_data,
        format="json"
    )

    print("response data", res)

    assert res.status_code == test_data["expected_status_code"]


@pytest.mark.django_db
@pytest.mark.parametrize("requested_date", [
    "2023-07-06", "2023-03-05", "2022-09-16"
])
def test_update_ideas_entry_incorrect_date(
    authenticated_user,
    requested_date
):
    """
    GIVEN a Django application
    WHEN the user requests to update an ideas entry with an incorrect date
    THEN the ideas entry is not and permission denied
    """
    (client, *_) = authenticated_user

    res = client.put(
        f"/api/ideas/{requested_date}/1/",
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
            "content entry": "I am healthy. My studies are going well. I am free and strong.",
        },
        "expected_status_code": 400
    }
])
def test_update_ideas_entry_invalid_json(
    authenticated_user,
    add_ideas_entry,
    test_data
):
    """
    GIVEN a Django application
    WHEN the user requests to update an ideas entry with invalid JSON
    THEN the ideas entry is not updated
    """
    client, user = authenticated_user

    current_date = date.today()

    ideas_entry = add_ideas_entry(
        content="Dentist",
        user=user,
    )

    res = client.put(
        f"/api/ideas/{current_date}/{ideas_entry.id}/",
        test_data["payload"],
        format="json"
    )

    assert res.status_code == test_data["expected_status_code"]
