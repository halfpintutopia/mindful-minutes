import json
from datetime import time

from django.urls import reverse

from rest_framework import status

import pytest

from journal.models import UserSettings


@pytest.mark.django_db
def test_add_user_settings(authenticated_user):
    """
    GIVEN a Django application
    WHEN the user sets their user settings for the first time
    THEN a new user settings object is created
    """
    client, user = authenticated_user

    url = reverse("user-settings", args=[user.slug])

    client.force_authenticate(user=user)

    data = {
        "user": user.id,
        "start_week_day": 1,
        "morning_check_in": time(9, 0).strftime("%H:%M:%S"),
        "evening_check_in": time(17, 0).strftime("%H:%M:%S")
    }

    res = client.post(
        url,
        json.dumps(data),
        content_type="application/json"
    )

    assert res.status_code == status.HTTP_201_CREATED
    assert res.data.get("user") == data["user"]
    assert res.data.get("start_week_day") == data["start_week_day"]
    assert res.data.get("morning_check_in") == data["morning_check_in"]
    assert res.data.get("evening_check_in") == data["evening_check_in"]


@pytest.mark.django_db
@pytest.mark.parametrize("test_data", [
    {
        "payload": {
            "start_week_day": 1,
            "morning_check_in": time(9, 0).strftime("%H:%M:%S")
        }
    },
    {
        "payload": {
            "start_week_day": 1,
            "evening_check_in": time(17, 0).strftime("%H:%M:%S")
        }
    },
    {
        "payload": {
            "morning_check_in": time(9, 0).strftime("%H:%M:%S"),
            "evening_check_in": time(17, 0).strftime("%H:%M:%S")
        }
    },
    {
        "payload": {}
    },
    {
        "payload": {
            "start week day": 1,
            "morning check in": time(9, 0).strftime("%H:%M:%S"),
            "evening check in": time(17, 0).strftime("%H:%M:%S")
        }
    }
])
def test_add_user_settings_invalid_data(authenticated_user, test_data):
    """
    GIVEN a Django application
    WHEN the user sets their user settings for the first time
    THEN a new settings object is not create, a 400 is returned
    """
    client, user = authenticated_user

    url = reverse("user-settings", args=[user.slug])

    client.force_authenticate(user=user)

    test_data["payload"]["user"] = user.id

    payload = json.dumps(test_data["payload"])

    res = client.post(
        url,
        payload,
        content_type="application/json"
    )

    assert res.status_code == status.HTTP_400_BAD_REQUEST


@pytest.mark.django_db
def test_get_user_settings(authenticated_user, add_user_settings):
    """
    GIVEN a Django application
    WHEN the user requests their user settings
    THEN the user settings are returned
    """
    client, user = authenticated_user

    start_week_day = 1
    morning_check_in = time(8, 0)
    evening_check_in = time(19, 0)

    add_user_settings(
        user=user,
        start_week_day=start_week_day,
        morning_check_in=morning_check_in,
        evening_check_in=evening_check_in
    )

    client.force_authenticate(user=user)

    url = reverse("user-settings", args=[user.slug])

    res = client.get(
        url
    )

    assert res.status_code == status.HTTP_200_OK
    assert res.data["user"] == user.id
    assert res.data["start_week_day"] == start_week_day
    assert res.data["morning_check_in"] == morning_check_in.strftime(
        "%H:%M:%S")
    assert res.data["evening_check_in"] == evening_check_in.strftime(
        "%H:%M:%S")


@pytest.mark.django_db
def test_get_user_settings_incorrect_id(authenticated_user):
    """
    GIVEN a Django application
    WHEN the user requests their user settings
    THEN the user settings are not returned and a 404 is returned
    """
    client, user = authenticated_user

    invalid_id = 1245
    url = reverse("user-settings", args=[invalid_id])

    client.force_authenticate(user=user)

    res = client.get(
        url
    )

    assert res.status_code == status.HTTP_403_FORBIDDEN


@pytest.mark.django_db
def test_remove_user_settings(authenticated_user, add_user_settings):
    """
    GIVEN a Django application
    WHEN the user request to delete their user settings
    THEN the user setting are deleted
    """
    client, user = authenticated_user

    start_week_day = 1
    morning_check_in = time(8, 0)
    evening_check_in = time(19, 0)

    add_user_settings(
        user=user,
        start_week_day=start_week_day,
        morning_check_in=morning_check_in,
        evening_check_in=evening_check_in
    )

    url = reverse("user-settings", args=[user.slug])

    client.force_authenticate(user=user)

    res = client.delete(
        url
    )

    assert res.status_code == status.HTTP_204_NO_CONTENT

    assert not UserSettings.objects.filter(user=user).exists()


@pytest.mark.django_db
def test_remove_user_settings_incorrect_id(authenticated_user, add_user_settings):
    """
    GIVEN a Django application
    WHEN the user requests to remove a user with an incorrect id
    THEN the user is not found, a 404 is returned
    """
    client, user = authenticated_user

    start_week_day = 1
    morning_check_in = time(8, 0)
    evening_check_in = time(19, 0)

    add_user_settings(
        user=user,
        start_week_day=start_week_day,
        morning_check_in=morning_check_in,
        evening_check_in=evening_check_in
    )

    invalid_id = 12457

    url = reverse("user-settings", args=[invalid_id])

    client.force_authenticate(user=user)

    res = client.delete(
        url
    )

    assert res.status_code == status.HTTP_403_FORBIDDEN


@pytest.mark.django_db
@pytest.mark.parametrize("test_data", [
    {
        "payload": {
            "start_week_day": 7,
            "morning_check_in": time(8, 0).strftime("%H:%M:%S"),
            "evening_check_in": time(19, 0).strftime("%H:%M:%S")
        }
    },
    {
        "payload": {
            "start_week_day": 1,
            "morning_check_in": time(9, 0).strftime("%H:%M:%S"),
            "evening_check_in": time(19, 0).strftime("%H:%M:%S")
        }
    },
    {
        "payload": {
            "start_week_day": 1,
            "morning_check_in": time(8, 0).strftime("%H:%M:%S"),
            "evening_check_in": time(17, 0).strftime("%H:%M:%S")
        }
    },
    {
        "payload": {
            "start_week_day": 7,
            "morning_check_in": time(9, 0).strftime("%H:%M:%S"),
            "evening_check_in": time(17, 0).strftime("%H:%M:%S")
        }
    }
])
def test_update_user_settings(authenticated_user, add_user_settings, test_data):
    """
    GIVEN a Django application
    WHEN a user requests to update their settings
    THEN the user settings are updated
    """
    client, user = authenticated_user

    start_week_day = 1
    morning_check_in = time(8, 0)
    evening_check_in = time(19, 0)

    add_user_settings(
        user=user,
        start_week_day=start_week_day,
        morning_check_in=morning_check_in,
        evening_check_in=evening_check_in
    )
    url = reverse("user-settings", args=[user.slug])

    client.force_authenticate(user=user)

    test_data["payload"]["user"] = user.id

    payload = json.dumps(test_data["payload"])

    res = client.put(
        url,
        payload,
        content_type="application/json",
    )

    assert res.status_code == status.HTTP_200_OK
    assert res.data["start_week_day"] == test_data["payload"]["start_week_day"]
    assert res.data["morning_check_in"] == test_data["payload"]["morning_check_in"]
    assert res.data["evening_check_in"] == test_data["payload"]["evening_check_in"]


@pytest.mark.django_db
def test_update_user_settings_incorrect_id(authenticated_user, add_user_settings):
    """
    GIVEN a Django application
    WHEN a user requests to update user settings with an incorrect id
    THEN the user settings are not found, and updating is not allowed, a 403 is returned
    """
    client, user = authenticated_user

    start_week_day = 1
    morning_check_in = time(8, 0)
    evening_check_in = time(19, 0)

    invalid_id = 12547

    add_user_settings(
        user=user,
        start_week_day=start_week_day,
        morning_check_in=morning_check_in,
        evening_check_in=evening_check_in
    )

    payload = {
        "start_week_day": 7,
        "morning_check_in": time(9, 0).strftime("%H:%M:%S"),
        "evening_check_in": time(17, 0).strftime("%H:%M:%S")
    }

    url = reverse("user-settings", args=[invalid_id])

    res = client.put(
        url,
        json.dumps(payload),
        content_type="application/json"
    )

    assert res.status_code == status.HTTP_403_FORBIDDEN


@pytest.mark.django_db
@pytest.mark.parametrize("test_data", [
    {
        "payload": {
            "morning_check_in": time(8, 0).strftime("%H:%M:%S"),
            "evening_check_in": time(19, 0).strftime("%H:%M:%S")
        }
    },
    {
        "payload": {
            "start_week_day": 1,
            "evening_check_in": time(19, 0).strftime("%H:%M:%S")
        }
    },
    {
        "payload": {
            "start_week_day": 1,
            "morning_check_in": time(8, 0).strftime("%H:%M:%S"),
        }
    },
    {
        "payload": {
            "start week day": 7,
            "morning check in": time(9, 0).strftime("%H:%M:%S"),
            "evening check in": time(17, 0).strftime("%H:%M:%S")
        }
    },
    {
        "payload": {
            "start": 7,
            "morning": time(9, 0).strftime("%H:%M:%S"),
            "evening": time(17, 0).strftime("%H:%M:%S")
        }
    }
])
def test_update_user_settings_invalid_data(authenticated_user, add_user_settings, test_data):
    """
    GIVEN a Django application
    WHEN a user request to update their settings with invalid data
    THEN the user settings are are not updated and a 400 is returned
    """
    client, user = authenticated_user

    start_week_day = 1
    morning_check_in = time(8, 0)
    evening_check_in = time(19, 0)

    add_user_settings(
        user=user,
        start_week_day=start_week_day,
        morning_check_in=morning_check_in,
        evening_check_in=evening_check_in
    )

    url = reverse("user-settings", args=[user.slug])

    test_data["payload"]["user"] = user.id

    payload = json.dumps(test_data["payload"])

    res = client.put(
        url,
        payload,
        content_type="application/json"
    )

    assert res.status_code == status.HTTP_400_BAD_REQUEST
