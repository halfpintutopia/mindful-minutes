import json
import random
from datetime import date

import pytest
from django.urls import reverse

from freezegun import freeze_time
from rest_framework import status


@pytest.mark.django_db
def test_get_list_of_emotion_entries(authenticated_user, add_emotion_entry):
    """
    GIVEN a Django application
    WHEN a user requests a list of all emotion entries
    THEN the user should receive a list of all emotion entries
    """
    client, user = authenticated_user

    emotions = ["good", "great", "good", "bad", "awful", "excellent"]

    for emotion in emotions:
        add_emotion_entry(user=user, emotion=emotion)

    url = reverse("emotion-entry-list", args=[user.slug])

    res = client.get(url)

    assert res.status_code == status.HTTP_200_OK


@pytest.mark.django_db
def test_add_emotion_entry(authenticated_user):
    """
    GIVEN a Django application
    WHEN a user adds a new emotion
    THEN the emotion is created and associated with the user
    """
    client, user = authenticated_user

    current_date = date.today()

    payload = {"emotion": "great"}

    url = reverse("emotion-entry-date-list", args=[user.slug, current_date])

    res = client.post(
        url, data=json.dumps(payload), content_type="application/json"
    )

    assert res.status_code == status.HTTP_201_CREATED


@pytest.mark.django_db
def test_add_emotion_entry_incorrect_date(authenticated_user):
    """
    GIVEN a Django application
    WHEN a user adds a new emotion that is not the current date
    THEN the emotion is not created
    """
    client, user = authenticated_user

    not_current_date = "2023-04-02"

    payload = {"emotion": "great"}

    url = reverse(
        "emotion-entry-date-list", args=[user.slug, not_current_date]
    )

    res = client.post(
        url, data=json.dumps(payload), content_type="application/json"
    )

    assert res.status_code == status.HTTP_403_FORBIDDEN


@pytest.mark.django_db
def test_add_emotion_entry_invalid_user(client, custom_user):
    """
    GIVEN a Django application
    WHEN a user adds a new emotion with in invalid user
    THEN the emotion is not created
    """
    current_date = date.today()

    payload = {"emotion": "great"}

    url = reverse(
        "emotion-entry-date-list", args=[custom_user.slug, current_date]
    )

    res = client.post(
        url, data=json.dumps(payload), content_type="application/json"
    )

    assert res.status_code == status.HTTP_403_FORBIDDEN


@pytest.mark.django_db
def test_get_single_emotion_entry_by_date(
    authenticated_user, add_emotion_entry
):
    """
    GIVEN a Django application
    WHEN a user requests to get an emotion by date
    THEN the emotion for the specified date is returned
    """
    client, user = authenticated_user

    emotion = "good"

    emotion_entry = add_emotion_entry(user=user, emotion=emotion)

    emotion_date = emotion_entry.created_on.strftime("%Y-%m-%d")

    url = reverse(
        "emotion-entry-detail",
        args=[user.slug, emotion_date, emotion_entry.id],
    )

    res = client.get(url)

    assert res.status_code == status.HTTP_200_OK
    assert res.data.get("emotion") == emotion
    assert res.data.get("user") == user.id


@pytest.mark.django_db
def test_delete_emotion_entry(authenticated_user, add_emotion_entry):
    """
    GIVEN a Django application
    WHEN a user deletes an existing emotion entry
    THEN the emotion is deleted and no longer accessible
    """
    client, user = authenticated_user

    emotion = "good"

    emotion_entry = add_emotion_entry(user=user, emotion=emotion)

    emotion_date = emotion_entry.created_on.strftime("%Y-%m-%d")

    url = reverse(
        "emotion-entry-detail",
        args=[user.slug, emotion_date, emotion_entry.id],
    )
    res = client.delete(url)

    assert res.status_code == status.HTTP_204_NO_CONTENT


@pytest.mark.django_db
def test_delete_emotion_entry_unauthenticated_user(
    authenticated_user, custom_user, add_emotion_entry
):
    """
    GIVEN a Django application
    WHEN a user attempts to delete an existing emotion that is not theirs
    THEN the emotion is not deleted
    """
    client, user = authenticated_user

    emotion = "good"

    emotion_entry = add_emotion_entry(user=custom_user, emotion=emotion)

    emotion_date = emotion_entry.created_on.strftime("%Y-%m-%d")

    url = reverse(
        "emotion-entry-detail",
        args=[custom_user.slug, emotion_date, emotion_entry.id],
    )

    res = client.delete(url)

    assert res.status_code == status.HTTP_403_FORBIDDEN


@pytest.mark.django_db
def test_delete_emotion_entry_invalid_id(
    authenticated_user, add_emotion_entry
):
    """
    GIVEN a Django application
    WHEN a user attempts to delete an emotion with an invalid id
    THEN the emotion is not deleted
    """
    client, user = authenticated_user

    emotion = "good"

    emotion_entry = add_emotion_entry(user=user, emotion=emotion)

    invalid_number = random.randint(10, 100)
    emotion_date = emotion_entry.created_on.strftime("%Y-%m-%d")

    url = reverse(
        "emotion-entry-detail",
        args=[user.slug, emotion_date, invalid_number],
    )

    res = client.delete(url)

    assert res.status_code == status.HTTP_404_NOT_FOUND


@pytest.mark.django_db
def test_delete_emotion_entry_not_current_date(
    authenticated_user, add_emotion_entry
):
    """
    GIVEN a Django application
    WHEN a user attempts to delete an emotion with an invalid id
    THEN the emotion is not deleted
    """
    client, user = authenticated_user

    emotion = "good"
    with freeze_time("2023-05-02 12:00:00"):
        emotion_entry = add_emotion_entry(user=user, emotion=emotion)

    emotion_date = emotion_entry.created_on.strftime("%Y-%m-%d")

    url = reverse(
        "emotion-entry-detail",
        args=[user.slug, emotion_date, emotion_entry.id],
    )

    res = client.delete(url)

    assert res.status_code == status.HTTP_403_FORBIDDEN


@pytest.mark.django_db
def test_update_emotion_entry(authenticated_user, add_emotion_entry):
    """
    GIVEN a Django application
    WHEN a user updates an existing emotion
    THEN the emotion is updated with the new data
    """
    client, user = authenticated_user

    emotion = "good"

    emotion_entry = add_emotion_entry(user=user, emotion=emotion)

    emotion_date = emotion_entry.created_on.strftime("%Y-%m-%d")

    payload = {"emotion": "excellent"}

    url = reverse(
        "emotion-entry-detail",
        args=[user.slug, emotion_date, emotion_entry.id],
    )

    res = client.put(url, data=payload)

    assert res.status_code == status.HTTP_200_OK


@pytest.mark.django_db
def test_update_emotion_entry_unauthenticated_user(
    authenticated_user, custom_user, add_emotion_entry
):
    """
    GIVEN a Django application
    WHEN a user updates an existing emotion that is not theirs
    THEN the emotion is not updated
    """
    client, user = authenticated_user

    emotion = "good"

    emotion_entry = add_emotion_entry(user=custom_user, emotion=emotion)

    emotion_date = emotion_entry.created_on.strftime("%Y-%m-%d")

    payload = {"emotion": "excellent"}

    url = reverse(
        "emotion-entry-detail",
        args=[custom_user.slug, emotion_date, emotion_entry.id],
    )

    res = client.put(url, data=payload)

    assert res.status_code == status.HTTP_403_FORBIDDEN
