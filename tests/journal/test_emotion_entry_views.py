import json
from datetime import date
# https://dennisokeeffe.medium.com/mocking-python-datetime-in-tests-with-freezegun-f5532307d6d6
from freezegun import freeze_time

from django.urls import reverse

from rest_framework import status

import pytest

from journal.models import EmotionEntry


@pytest.mark.django_db
def test_add_emotion_entry(authenticated_user):
    """
    GIVEN a Django application
    WHEN a user adds a new emotion
    THEN the emotion is created and associated with the user
    """
    (client, *_) = authenticated_user

    current_date = date.today()

    url = reverse("emotion-entry-list", args=[current_date])

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

    url = reverse("emotion-entry-list", args=[not_current_date])

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

    url = reverse("emotion-entry-list", args=[current_date])

    payload = {
        "emotion": "great"
    }

    res = client.post(
        url,
        data=json.dumps(payload),
        content_type="application/json"
    )

    assert res.status_code == status.HTTP_403_FORBIDDEN

