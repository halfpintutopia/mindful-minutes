from datetime import time

from django.contrib.auth import get_user_model

from journal.serializers import UserSettingsSerializer

User = get_user_model()


def test_valid_user_setting_serializer():
    """
    GIVEN a valid user settings serializer
    WHEN the data is passed to the serializer
    THEN the serializer should be valid
    """
    user = User.objects.create_user(email="normal@user.com")
    valid_serializer_data = {
        "user": user.pk,
        "start_week_day": 1,
        "morning_check_in": time(8, 30),
        "evening_check_in": time(20, 00)
    }
    serializer = UserSettingsSerializer(data=valid_serializer_data)
    assert serializer.is_valid()
    assert serializer.validated_data == valid_serializer_data
    assert serializer.data == valid_serializer_data
    assert serializer.errors == {}

def test_invalid_user_settings_serializer_missing_start_week_day():
    """
    GIVEN an invalid user settings serializer
    WHEN the data is passed to the serializer
    THEN the serializer should be invalid
    """
    user = User.objects.create_user(email="normal@user.com")
    invalid_serializer_data = {
        "user": user.pk,
        "morning_check_in": time(8, 30),
        "evening_check_in": time(20, 00)
    }
    serializer = UserSettingsSerializer(data=invalid_serializer_data)
    assert not serializer.is_valid()
    assert serializer.error == {
        "start_week_day": ["This field is required."]
    }

def test_invalid_user_settings_serializer_missing_morning_check_in():
    """
    GIVEN an invalid user settings serializer
    WHEN the data is passed to the serializer
    THEN the serializer should be invalid
    """
    user = User.objects.create_user(email="normal@user.com")
    invalid_serializer_data = {
        "user": user.pk,
        "start_week_day": 1,
        "evening_check_in": time(20, 00)
    }
    serializer = UserSettingsSerializer(data=invalid_serializer_data)
    assert not serializer.is_valid()
    assert serializer.error == {
        "morning_check_in": ["This field is required."]
    }

def test_invalid_user_settings_serializer_missing_evening_check_in():
    """
    GIVEN an invalid user settings serializer
    WHEN the data is passed to the serializer
    THEN the serializer should be invalid
    """
    user = User.objects.create_user(email="normal@user.com")
    invalid_serializer_data = {
        "user": user.pk,
        "start_week_day": 1,
        "morning_check_in": time(8, 30),
    }
    serializer = UserSettingsSerializer(data=invalid_serializer_data)
    assert not serializer.is_valid()
    assert serializer.error == {
        "evening_check_in": ["This field is required."]
    }
