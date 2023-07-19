import pytest

from journal.models import WinEntry


@pytest.mark.django_db
def test_create_win_entry(custom_user):
	"""
	GIVEN a win entry model
	WHEN creating a win entry
	THEN user should have successfully created a win entry
	"""
	win_entry = WinEntry.objects.create(
		user=custom_user,
		title="20 minutes of meditation."
		)
	win_entry.save()
	win_entries = WinEntry.objects.all()
	assert len(win_entries) == 1
	assert win_entries[0].user == custom_user
	assert win_entries[0].title == "20 minutes of meditation."
	assert isinstance(
		win_entries[0].title, str
		) and win_entries[0].title is not None
