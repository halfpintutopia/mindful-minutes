import pytest

from django.contrib.auth import get_user_model

from journal.models import AppointmentEntry, Target, Note, KnowledgeEntry, \
    GratitudeEntry, WinEntry, IdeasEntry, ImprovementEntry, EmotionEntry

User = get_user_model()


@pytest.fixture(scope="function")
def add_appointment_entry():
    """
    Fixture to crete an AppointmentEntry object in the database
    """
    def _add_appointment_entry(title, date, time_from, time_until, user):
        appointment_entry = AppointmentEntry.objects.create(
            user=user,
            title=title,
            date=date,
            time_from=time_from,
            time_until=time_until
        )
        return appointment_entry
    return _add_appointment_entry
