from datetime import date

import pytest

from journal.models import Target


@pytest.mark.django_db
def test_add_target(authenticated_user):
    """
    GIVEN a Django application
    WHEN the user requests to add an target
    THEN check that the target is added
    """
    target_entries = Target.objects.all()
    assert len(target_entries) == 0

    client, user = authenticated_user

    target_data = {
        "content": "20 minutes of meditation",
        "user": user.id,
    }

    res = client.post(
        "/api/targets/",
        target_data,
        format="json"
    )

    assert res.status_code == 201
    assert res.data["user"] == user.id
    assert res.data["content"] == "20 minutes of meditation"

    target_entries = Target.objects.all()
    assert len(target_entries) == 1


@pytest.mark.django_db
@pytest.mark.parametrize("payload, status_code", [
    [{}, 400],
    [{"content entry": "20 minutes of meditation"}, 400]
])
def test_add_target_invalid_json(authenticated_user, payload, status_code):
    """
    GIVEN a Django application
    WHEN the user requests to add an target with an invalid payload
    THEN the payload is not sent
    """
    target_entries = Target.objects.all()
    assert len(target_entries) == 0

    client, user = authenticated_user

    payload["user"] = user.id

    res = client.post(
        "/api/targets/",
        payload,
        format="json"
    )
    assert res.status_code == status_code

    target_entries = Target.objects.all()
    assert len(target_entries) == 0


@pytest.mark.django_db
@pytest.mark.django_db
@pytest.mark.parametrize("add_target_entry, endpoint, expected_content", [
    ["add_target_entry", "id", "20 minutes of meditation"],
    ["add_target_entry", "date", [
        "20 minutes of meditation",
        "20 minute cold shower",
        "Meet Stefan for lunch",
        "Read 30 minutes of Momo"
    ]]
])
def test_get_single_target_entry(authenticated_user, add_target_entry, endpoint, expected_content):
    """
    GIVEN a Django application
    WHEN the user requests to retrieve a single target by id or targets by date
    THEN check that the target is retrieved
    """
    client, user = authenticated_user

    target_entry_one = add_target_entry(
        content="20 minutes of meditation",
        user=user
    )

    target_entry_two = add_target_entry(
        content="20 minute cold shower",
        user=user,
    )

    target_entry_three = add_target_entry(
        content="Meet Stefan for lunch",
        user=user,
    )

    target_entry_four = add_target_entry(
        content="Read 30 minutes of Momo",
        user=user,
    )

    if endpoint == "id":
        res = client.get(
            f"/api/targets/id/{target_entry_one.id}/", format="json")

        assert res.status_code == 200
        assert res.data["user"] == user.id
        assert res.data["content"] == expected_content
    elif endpoint == "date":
        current_date = date.today()

        res = client.get(f"/api/targets/date/{current_date}/")

        assert res.status_code == 200
        assert res.data[0]["created_on"] == date.today()
        assert len(res.data) == len(expected_content)
        assert all(entry["content"] in expected_content for entry in res.data)


@pytest.mark.django_db
@pytest.mark.parametrize("invalid_id, status_code", [
    ["random", 404],
    [1234, 404]
])
def test_get_single_target_incorrect_id(authenticated_user, invalid_id, status_code):
    """
    GIVEN a Django application
    WHEN the user requests to retrieve an target with an incorrect id
    THEN check the target is not retrieved
    """
    (client, *_) = authenticated_user

    res = client.get(f"/api/targets/id/{invalid_id}/")

    assert res.status_code == status_code


@pytest.mark.django_db
def test_get_all_target_entries(authenticated_user, add_target_entry):
    """
    GIVEN a Django application
    WHEN the user requests to retrieve all targets
    THEN check all targets are retrieved
    """
    target_entries = Target.objects.all()
    assert len(target_entries) == 0

    client, user = authenticated_user

    target_entry_one = add_target_entry(
        content="20 minutes of meditation",
        user=user
    )

    target_entry_two = add_target_entry(
        content="20 minute cold shower",
        user=user,
    )

    res = client.get("/api/targets/")

    assert res.status_code == 200
    assert res.data[0]["content"] == "20 minutes of meditation"
    assert res.data[1]["content"] == "20 minute cold shower"

    target_entries = Target.objects.all()
    assert len(target_entries) == 2


@pytest.mark.django_db
def test_remove_target_entry(authenticated_user, add_target_entry):
    """
    GIVEN a Django application
    WHEN the user requests to remove an target
    THEN the target is removed
    """
    target_entries = Target.objects.all()
    assert len(target_entries) == 0

    client, user = authenticated_user

    target_entry = add_target_entry(
        content="20 minutes of meditation",
        user=user
    )

    res = client.get(f"/api/targets/id/{target_entry.id}/")
    assert res.status_code == 200
    assert res.data["content"] == "20 minutes of meditation"

    res_delete = client.delete(f"/api/targets/id/{target_entry.id}/")
    assert res_delete.status_code == 204

    res_retrieve = client.get(f"/api/targets/")
    assert res_retrieve.status_code == 200
    assert len(res_retrieve.data) == 0

    assert not Target.objects.filter(id=target_entry.id).exists()

    target_entries = Target.objects.all()
    assert len(target_entries) == 0


@pytest.mark.django_db
@pytest.mark.parametrize("incorrect_id, status_code", [
    ["random", 404],
    [12574, 404],
    ["98", 404]
])
def test_remove_target_invalid_id(authenticated_user, incorrect_id, status_code):
    """
    GIVEN a Django application
    WHEN the user requests to remove an target with an invalid id
    THEN the target is not removed
    """
    target_entries = Target.objects.all()
    assert len(target_entries) == 0

    (client, *_) = authenticated_user

    res = client.get(f"/api/targets/id/{incorrect_id}/")
    assert res.status_code == status_code

    updated_target_entries = Target.objects.all()
    assert len(target_entries) == len(updated_target_entries)
    assert len(updated_target_entries) == 0


@pytest.mark.django_db
def test_update_target_entry(authenticated_user, add_target_entry):
    """
    GIVEN a Django application
    WHEN the user requests to update an target
    THEN the target is updated
    """
    target_entries = Target.objects.all()
    assert len(target_entries) == 0

    client, user = authenticated_user

    target_entry = add_target_entry(
        content="20 minutes of meditation",
        user=user
    )

    res = client.put(
        f"/api/targets/id/{target_entry.id}/",
        {
            "content": "20 minutes of yoga",
            "user": user.id
        },
        format="json"
    )

    assert res.status_code == 200
    assert res.data["created_on"] == date.today()
    assert res.data["content"] == "20 minutes of yoga"

    res_check = client.get(f"/api/targets/id/{target_entry.id}/")
    assert res_check.status_code == 200
    assert res.data["created_on"] == date.today()
    assert res.data["content"] == "20 minutes of yoga"

    target_entries = Target.objects.all()
    assert len(target_entries) == 1


@pytest.mark.django_db
@pytest.mark.parametrize("incorrect_id, status_code", [
    ["random", 404],
    [12574, 404],
    ["98", 404]
])
def test_update_target_entry_incorrect_id(authenticated_user, incorrect_id, status_code):
    """
    GIVEN a Django application
    WHEN the user requests to update an target with an incorrect id
    THEN the target is not updated
    """
    (client, *_) = authenticated_user

    res = client.put(f"/api/targets/id/{incorrect_id}/")

    assert res.status_code == status_code


@pytest.mark.django_db
@pytest.mark.parametrize("add_target_entry, payload, status_code", [
    ["add_target_entry", {}, 400],
    ["add_target_entry", {
        "content entry": "20 minutes of yoga"
    }, 400],
], indirect=["add_target_entry"])
def test_update_target_entry_invalid_json(
    authenticated_user,
    add_target_entry,
    payload,
    status_code
):
    """
    GIVEN a Django application
    WHEN the user requests to update an target with invalid JSON
    THEN the target is not updated
    """
    client, user = authenticated_user

    target_entry = add_target_entry(
        content="20 minutes of meditation",
        user=user,
    )

    payload["user"] = user.id

    res = client.put(
        f"/api/targets/id/{target_entry.id}/",
        payload,
        format="json"
    )

    assert res.status_code == status_code
