from datetime import time

import pytest

from django.contrib.auth import get_user_model

from journal.serializers import UserSettingsSerializer

User = get_user_model()


@pytest.mark.django_db
def test_valid_user_setting_serializer():
    """
    GIVEN a valid user settings serializer
    WHEN the data is passed to the serializer
    THEN the serializer should be valid
    """
    valid_serializer_data = {
        "start_week_day": 1,
        "morning_check_in": time(8, 30),
        "evening_check_in": time(20, 0)
    }
    serializer = UserSettingsSerializer(data=valid_serializer_data)
    assert serializer.is_valid()
    assert serializer.validated_data == valid_serializer_data
    assert serializer.data == {
        "start_week_day": 1,
        "morning_check_in": time(8, 30).strftime("%H:%M:%S"),
        "evening_check_in": time(20, 0).strftime("%H:%M:%S")
    }
    assert serializer.errors == {}


@pytest.mark.django_db
def test_invalid_user_settings_serializer_missing_start_week_day():
    """
    GIVEN an invalid user settings serializer
    WHEN the data is passed to the serializer
    THEN the serializer should be invalid
    """
    invalid_serializer_data = {
        "morning_check_in": time(8, 30),
        "evening_check_in": time(20, 00)
    }
    serializer = UserSettingsSerializer(data=invalid_serializer_data)
    assert not serializer.is_valid()

    print("validated_data", invalid_serializer_data)
    print("data", serializer.data)

    assert serializer.data == invalid_serializer_data
    assert serializer.errors == {
        "start_week_day": ["This field is required."]
    }


@pytest.mark.django_db
def test_invalid_user_settings_serializer_missing_morning_check_in():
    """
    GIVEN an invalid user settings serializer
    WHEN the data is passed to the serializer
    THEN the serializer should be invalid
    """
    invalid_serializer_data = {
        "start_week_day": 1,
        "evening_check_in": time(20, 00)
    }
    serializer = UserSettingsSerializer(data=invalid_serializer_data)
    assert not serializer.is_valid()
    assert serializer.data == invalid_serializer_data
    assert serializer.errors == {
        "morning_check_in": ["This field is required."]
    }


@pytest.mark.django_db
def test_invalid_user_settings_serializer_missing_evening_check_in():
    """
    GIVEN an invalid user settings serializer
    WHEN the data is passed to the serializer
    THEN the serializer should be invalid
    """
    invalid_serializer_data = {
        "start_week_day": 1,
        "morning_check_in": time(8, 30)
    }
    serializer = UserSettingsSerializer(data=invalid_serializer_data)
    assert not serializer.is_valid()
    assert serializer.data == invalid_serializer_data
    assert serializer.errors == {
        "evening_check_in": ["This field is required."]
    }
