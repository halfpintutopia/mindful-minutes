from datetime import date
# https://dennisokeeffe.medium.com/mocking-python-datetime-in-tests-with-freezegun-f5532307d6d6
from freezegun import freeze_time

import pytest

from journal.models import GratitudeEntry


@pytest.mark.django_db
def test_add_gratitude_entry(authenticated_user):
    """
    GIVEN a Django application
    WHEN the user requests to add an gratitude entry
    THEN check that the gratitude entry is added
    """
    gratitude_entries = GratitudeEntry.objects.all()
    assert len(gratitude_entries) == 0

    current_date = date.today()

    client, user = authenticated_user

    gratitude_data = {
        "content": "I am healthy. My studies are going well. I am free and strong.",
        "user": user.id,
    }

    res = client.post(
        f"/api/gratitude/{current_date}/",
        gratitude_data,
        format="json"
    )

    print("Response data", res.data)

    assert res.status_code == 201
    assert res.data["user"] == user.id
    assert res.data["content"] == "I am healthy. My studies are going well. I am free and strong."

    gratitude_entries = GratitudeEntry.objects.all()
    assert len(gratitude_entries) == 1


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
def test_add_gratitude_entry_incorrect_json(authenticated_user, test_data):
    """
    GIVEN a Django application
    WHEN the user requests to add an gratitude entry with an invalid payload
    THEN the payload is not sent
    """
    gratitude_entries = GratitudeEntry.objects.all()
    assert len(gratitude_entries) == 0

    current_date = date.today()

    client, user = authenticated_user

    test_data["payload"]["user"] = user.id

    res = client.post(
        f"/api/gratitude/{current_date}/",
        test_data["payload"],
        format="json"
    )
    assert res.status_code == 400

    gratitude_entries = GratitudeEntry.objects.all()
    assert len(gratitude_entries) == 0


@pytest.mark.django_db
@pytest.mark.parametrize("date_param", ["2023-07-01", "2023-06-20"])
def test_add_gratitude_entry_not_current_date(
    authenticated_user,
    date_param
):
    """
    GIVEN a Django application
    WHEN the user attempts to add an gratitude entry on a date,
    that is not the current date
    THEN the gratitude entry is not created
    """
    gratitude_entries = GratitudeEntry.objects.all()
    assert len(gratitude_entries) == 0

    client, user = authenticated_user

    gratitude_data = {
        "content": "I am healthy. My studies are going well. I am free and strong.",
        "user": user.id,
    }

    res = client.post(
        f"/api/gratitude/{date_param}/",
        gratitude_data,
        format="json"
    )

    assert res.status_code == 403

    gratitude_entries = GratitudeEntry.objects.all()
    assert len(gratitude_entries) == 0


@pytest.mark.django_db
def test_get_single_gratitude_entry(
    authenticated_user,
    add_gratitude_entry
):
    """
    GIVEN a Django application
    WHEN the user requests to retrieve an gratitude entry
    THEN check that the gratitude entry is retrieved
    """
    current_date = date.today()

    client, user = authenticated_user

    gratitude = add_gratitude_entry(
        content="I am healthy. My studies are going well. I am free and strong.",
        user=user,
    )

    res = client.get(
        f"/api/gratitude/{current_date}/{gratitude.id}/",
        format="json"
    )

    assert res.status_code == 200
    assert res.data["user"] == user.id
    assert res.data["content"] == "I am healthy. My studies are going well. I am free and strong."


@pytest.mark.django_db
@pytest.mark.parametrize("invalid_id", ["random", "1", 14258])
def test_get_single_gratitude_entry_incorrect_id(
    authenticated_user,
    invalid_id
):
    """
    GIVEN a Django application
    WHEN the user requests to retrieve an gratitude entry with an incorrect id
    THEN check the gratitude entry is not retrieved
    """
    (client, *_) = authenticated_user

    current_date = date.today()

    res = client.get(f"/api/gratitude/{current_date}/{invalid_id}/")

    assert res.status_code == 404


@pytest.mark.django_db
def test_get_all_gratitude_entries_by_current_date(
    authenticated_user,
    add_gratitude_entry
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
        content="I am healthy. My studies are going well. I am free and strong.",
        user=user,
    )

    res = client.get(f"/api/gratitude/{str(current_date)}/")

    assert res.status_code == 200
    assert res.data[0]["created_on"] == str(current_date)

    gratitude_entries = GratitudeEntry.objects.filter(
        created_on__date=current_date)
    assert len(gratitude_entries) == 1


@pytest.mark.django_db
@pytest.mark.parametrize("created_on_timestamp", [
    "2023-07-06 12:00:00",
    "2023-06-04 10:30:00",
    "2022-07-09 19:45:00",
])
def test_get_all_gratitude_entries_by_date(
    authenticated_user,
    add_gratitude_entry,
    created_on_timestamp
):
    """
    GIVEN a Django application
    WHEN the user requests to retrieve all gratitude entries by date
    THEN check all gratitude entries are retrieved
    """
    with freeze_time(created_on_timestamp):
        gratitude_entries = GratitudeEntry.objects.all()
        assert len(gratitude_entries) == 0

        current_date = date.today()

        client, user = authenticated_user

        add_gratitude_entry(
            content="I am healthy. My studies are going well. I am free and strong.",
            user=user,
        )

        res = client.get(f"/api/gratitude/{str(current_date)}/")

        assert res.status_code == 200
        assert res.data[0]["created_on"] == str(current_date)

        gratitude_entries = GratitudeEntry.objects.filter(
            created_on__date=current_date)
        assert len(gratitude_entries) == 1


@pytest.mark.django_db
def test_remove_gratitude_entry(
    authenticated_user,
    add_gratitude_entry
):
    """
    GIVEN a Django application
    WHEN the user requests to remove an gratitude entry
    THEN the gratitude entry is removed
    """
    gratitude_entries = GratitudeEntry.objects.all()
    assert len(gratitude_entries) == 0

    current_date = date.today()

    client, user = authenticated_user

    gratitude_entry = add_gratitude_entry(
        content="I am healthy. My studies are going well. I am free and strong.",
        user=user,
    )

    res = client.get(
        f"/api/gratitude/{current_date}/{gratitude_entry.id}/",
        format="json"
    )

    assert res.status_code == 200
    assert res.data["content"] == "I am healthy. My studies are going well. I am free and strong."

    res_delete = client.delete(
        f"/api/gratitude/{current_date}/{gratitude_entry.id}/",
        format="json"
    )

    assert res_delete.status_code == 204

    res_retrieve = client.get(
        f"/api/gratitude/{current_date}/", format="json")

    assert res_retrieve.status_code == 200
    assert len(res_retrieve.data) == 0

    assert not GratitudeEntry.objects.filter(id=gratitude_entry.id).exists()

    gratitude_entries = GratitudeEntry.objects.all()
    assert len(gratitude_entries) == 0


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
def test_remove_gratitude_invalid_id(
    authenticated_user,
    test_data
):
    """
    GIVEN a Django application
    WHEN the user requests to remove an gratitude entry with an invalid id
    THEN the gratitude entry is not removed
    """
    gratitude_entries = GratitudeEntry.objects.all()
    assert len(gratitude_entries) == 0

    current_date = date.today()

    (client, *_) = authenticated_user

    res = client.delete(
        f"/api/gratitude/{current_date}/{test_data['incorrect_id']}/",
        format="json"
    )

    assert res.status_code == test_data["expected_status_code"]

    updated_gratitude_entries = GratitudeEntry.objects.all()
    assert len(gratitude_entries) == len(updated_gratitude_entries)
    assert len(updated_gratitude_entries) == 0


@pytest.mark.django_db
@pytest.mark.parametrize("requested_date", [
    "2023-07-06", "2023-03-05", "2022-09-16"
])
def test_remove_gratitude_not_current_date(
    authenticated_user, requested_date
):
    """
    GIVEN a Django application
    WHEN the user requests to remove an gratitude entry when the date is not today
    THEN the gratitude entry is not removed
    """
    gratitude_entries = GratitudeEntry.objects.all()
    assert len(gratitude_entries) == 0

    (client, *_) = authenticated_user

    res = client.delete(
        f"/api/gratitude/{requested_date}/1/", format="json")

    assert res.status_code == 403

    updated_gratitude_entries = GratitudeEntry.objects.all()
    assert len(gratitude_entries) == len(updated_gratitude_entries)
    assert len(updated_gratitude_entries) == 0


@pytest.mark.django_db
@pytest.mark.parametrize("test_data", [
    {
        "payload": {
            "content": "I am healthy. My studies are going well. I am free and strong. Refactored code with new gratitude",
        }
    },
    {
        "payload": {
            "content": "Read a chapter of Eloquent JavaScript and was able to explain this to another colleague",
        }
    }
])
def test_update_gratitude_entry(
    authenticated_user,
    add_gratitude_entry,
    test_data
):
    """
    GIVEN a Django application
    WHEN the user requests to update an gratitude entry
    THEN the gratitude entry is updated
    """
    gratitude_entries = GratitudeEntry.objects.all()
    assert len(gratitude_entries) == 0

    current_date = date.today()

    client, user = authenticated_user

    gratitude_entry = add_gratitude_entry(
        content="I am healthy. My studies are going well. I am free and strong.",
        user=user,
    )

    test_data["payload"]["user"] = user.id

    res = client.put(
        f"/api/gratitude/{current_date}/{gratitude_entry.id}/",
        test_data["payload"],
        format="json"
    )

    assert res.status_code == 200
    assert res.data["content"] == test_data["payload"]["content"]

    res_check = client.get(
        f"/api/gratitude/{current_date}/{gratitude_entry.id}/",
        format="json"
    )

    assert res_check.status_code == 200
    assert res.data["content"] == test_data["payload"]["content"]

    gratitude_entries = GratitudeEntry.objects.all()
    assert len(gratitude_entries) == 1


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
def test_update_gratitude_entry_incorrect_data(
    authenticated_user,
    add_gratitude_entry,
    test_data
):
    """
    GIVEN a Django application
    WHEN the user requests to update an gratitude entry with an incorrect id
    THEN the gratitude entry is not updated
    """
    client, user = authenticated_user

    current_date = date.today()

    add_gratitude_entry(
        content="I am healthy. My studies are going well. I am free and strong.",
        user=user,
    )

    gratitude_data = {
        "content": "Read a chapter of Eloquent JavaScript and was able to explain this to another colleague",
        "user": user.id,
    }

    res = client.put(
        f"/api/gratitude/{current_date}/{test_data['incorrect_id']}/",
        gratitude_data,
        format="json"
    )

    print("response data", res)

    assert res.status_code == test_data["expected_status_code"]


@pytest.mark.django_db
@pytest.mark.parametrize("requested_date", [
    "2023-07-06", "2023-03-05", "2022-09-16"
])
def test_update_gratitude_entry_incorrect_date(
    authenticated_user,
    requested_date
):
    """
    GIVEN a Django application
    WHEN the user requests to update an gratitude entry with an incorrect date
    THEN the gratitude entry is not and permission denied
    """
    (client, *_) = authenticated_user

    res = client.put(
        f"/api/gratitude/{requested_date}/1/",
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
def test_update_gratitude_entry_invalid_json(
    authenticated_user,
    add_gratitude_entry,
    test_data
):
    """
    GIVEN a Django application
    WHEN the user requests to update an gratitude entry with invalid JSON
    THEN the gratitude entry is not updated
    """
    client, user = authenticated_user

    current_date = date.today()

    gratitude_entry = add_gratitude_entry(
        content="Dentist",
        user=user,
    )

    res = client.put(
        f"/api/gratitude/{current_date}/{gratitude_entry.id}/",
        test_data["payload"],
        format="json"
    )

    assert res.status_code == test_data["expected_status_code"]
