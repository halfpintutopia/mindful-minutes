from datetime import time

import pytest

from journal.models import UserSettings
from journal.serializers import UserSettingsSerializer


@pytest.mark.django_db
def test_user_settings_serializer(custom_user):
    """
    GIVEN a UserSettings model
    WHEN a new user settings are created
    THEN check the, start_week_day,
    morning_check_in, evening_check_in
    """
    start_week_day = 1
    morning_check_in = time(9, 0)
    evening_check_in = time(17, 0)

    user_settings = UserSettings.objects.create(
        user=custom_user,
        start_week_day=start_week_day,
        morning_check_in=morning_check_in,
        evening_check_in=evening_check_in
    )

    serializer = UserSettingsSerializer(user_settings)

    assert serializer.data.get("user") == custom_user.id
    assert serializer.data.get("start_week_day") == start_week_day
    assert serializer.data.get(
        "morning_check_in") == morning_check_in.strftime("%H:%M:%S")
    assert serializer.data.get(
        "evening_check_in") == evening_check_in.strftime("%H:%M:%S")


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
    assert not serializer.errors


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
    assert serializer.validated_data == {}
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
    assert serializer.validated_data == {}
    assert serializer.data == {
        "start_week_day": 1,
        "evening_check_in": time(20, 00)
    }
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
    assert serializer.validated_data == {}
    assert serializer.data == invalid_serializer_data
    assert serializer.errors == {
        "evening_check_in": ["This field is required."]
    }
