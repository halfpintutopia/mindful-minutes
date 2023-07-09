import json
from datetime import date
# https://dennisokeeffe.medium.com/mocking-python-datetime-in-tests-with-freezegun-f5532307d6d6
from freezegun import freeze_time

from django.urls import reverse

from rest_framework import status

import pytest

from journal.models import EmotionEntry


@pytest.mark.django_db
def test_get_list_of_emotion_entries(authenticated_user, add_emotion_entry):
    """
    GIVEN a Django application
    WHEN a user requests a list of all emotion entries
    THEN the user should receive a list of all emotion entries
    """
    client, user = authenticated_user

    emotion = "good"

    emotion_entry = add_emotion_entry(
        user=user,
        emotion=emotion
    )

    url = reverse("emotion-entry-list-all")

    res = client.get(
        url
    )

    assert res.status_code == status.HTTP_200_OK


@pytest.mark.django_db
def test_add_emotion_entry(authenticated_user):
    """
    GIVEN a Django application
    WHEN a user adds a new emotion
    THEN the emotion is created and associated with the user
    """
    (client, *_) = authenticated_user

    current_date = date.today()

    url = reverse("emotion-entry-list-date", args=[current_date])

    payload = {
        "emotion": "great"
    }

    res = client.post(
        url,
        data=json.dumps(payload),
        content_type="application/json"
    )

    assert res.status_code == status.HTTP_201_CREATED


@pytest.mark.django_db
def test_add_emotion_entry_incorrect_date(authenticated_user):
    """
    GIVEN a Django application
    WHEN a user adds a new emotion that is not the current date
    THEN the emotion is not created
    """
    (client, *_) = authenticated_user

    not_current_date = "2023-04-02"

    url = reverse("emotion-entry-list-date", args=[not_current_date])

    payload = {
        "emotion": "great"
    }

    res = client.post(
        url,
        data=json.dumps(payload),
        content_type="application/json"
    )

    assert res.status_code == status.HTTP_403_FORBIDDEN


@pytest.mark.django_db
def test_add_emotion_entry_invalid_user(client):
    """
    GIVEN a Django application
    WHEN a user adds a new emotion with in invalid user
    THEN the emotion is not created
    """
    current_date = date.today()

    url = reverse("emotion-entry-list-date", args=[current_date])

    payload = {
        "emotion": "great"
    }

    res = client.post(
        url,
        data=json.dumps(payload),
        content_type="application/json"
    )

    assert res.status_code == status.HTTP_403_FORBIDDEN


@pytest.mark.django_db
def test_get_single_emotion_entry_by_date(authenticated_user, add_emotion_entry):
    """
    GIVEN a Django application
    WHEN a user requests to get an emotion by date
    THEN the emotion for the specified date is returned
    """
    client, user = authenticated_user

    emotion = "good"

    emotion_entry = add_emotion_entry(
        user=user,
        emotion=emotion
    )

    date = emotion_entry.created_on.strftime("%Y-%m-%d")

    url = reverse("emotion-entry-detail-single", args=[date, emotion_entry.id])

    res = client.get(url)

    assert res.status_code == status.HTTP_200_OK
    assert res.data.get("emotion") == emotion
    assert res.data.get("user") == user.id


# @pytest.mark.django_db
