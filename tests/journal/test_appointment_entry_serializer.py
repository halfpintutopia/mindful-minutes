from datetime import time, date

import pytest

from journal.serializers import AppointmentEntrySerializer


def test_valid_appointment_entry_serializer():
    """
    GIVEN a valid appointment entry serializer
    WHEN the data is passed to the serializer
    THEN the serializer should be valid
    """
    valid_serializer_data = {
        "title": "Dentist",
        "date": date(2023, 7, 6),
        "time_from": time(10, 0),
        "time_until": time(11, 0)
    }
    serializer = AppointmentEntrySerializer(data=valid_serializer_data)
    assert serializer.is_valid()
    print("validated_data:", serializer.validated_data)
    print("data:", serializer.data)
    assert serializer.validated_data == valid_serializer_data
    assert serializer.data == {
        "title": "Dentist",
        "date": date(2023, 7, 6).strftime("%Y-%m-%d"),
        "time_from": time(10, 0).strftime("%H:%M:%S"),
        "time_until": time(11, 0).strftime("%H:%M:%S")
    }
    assert not serializer.errors


def test_missing_title_appointment_entry_serializer():
    """
    GIVEN an invalid appointment entry serializer
    WHEN the data is passed to the serializer with missing title
    THEN the serializer should be invalid
    """
    invalid_serializer_data = {
        "date": date(2023, 7, 6),
        "time_from": time(10, 0),
        "time_until": time(11, 0)
    }
    serializer = AppointmentEntrySerializer(data=invalid_serializer_data)
    assert not serializer.is_valid()
    assert serializer.validated_data == {}
    assert serializer.data == invalid_serializer_data
    assert serializer.errors == {
        "title": ["This field is required."]
    }


def test_missing_date_appointment_entry_serializer():
    """
    GIVEN an invalid appointment entry serializer
    WHEN the data is passed to the serializer with missing date
    THEN the serializer should be invalid
    """
    invalid_serializer_data = {
        "title": "Dentist",
        "time_from": time(10, 0),
        "time_until": time(11, 0)
    }
    serializer = AppointmentEntrySerializer(data=invalid_serializer_data)
    assert not serializer.is_valid()
    assert serializer.validated_data == {}
    assert serializer.data == invalid_serializer_data
    assert serializer.errors == {
        "date": ["This field is required."]
    }


def test_missing_time_from_appointment_entry_serializer():
    """
    GIVEN an invalid appointment entry serializer
    WHEN the data is passed to the serializer with missing from time
    THEN the serializer should be invalid
    """
    invalid_serializer_data = {
        "title": "Dentist",
        "date": date(2023, 7, 6),
        "time_until": time(11, 0)
    }
    serializer = AppointmentEntrySerializer(data=invalid_serializer_data)
    assert not serializer.is_valid()
    assert serializer.validated_data == {}
    assert serializer.data == invalid_serializer_data
    assert serializer.errors == {
        "time_from": ["This field is required."]
    }


def test_missing_time_until_appointment_entry_serializer():
    """
    GIVEN an invalid appointment entry serializer
    WHEN the data is passed to the serializer with missing until time
    THEN the serializer should be invalid
    """
    invalid_serializer_data = {
        "title": "Dentist",
        "date": date(2023, 7, 6),
        "time_from": time(10, 0),
    }
    serializer = AppointmentEntrySerializer(data=invalid_serializer_data)
    assert not serializer.is_valid()
    assert serializer.validated_data == {}
    assert serializer.data == invalid_serializer_data
    assert serializer.errors == {
        "time_until": ["This field is required."]
    }
