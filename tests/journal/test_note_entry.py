import pytest

from journal.models import NoteEntry


@pytest.mark.django_db
def test_create_note(custom_user):
	"""
	GIVEN a note model
	WHEN creating a note
	THEN user should have successfully created a note
	"""
	note = NoteEntry.objects.create(
		user=custom_user,
		content="I have to order 'Eloquent JavaScript'",
		)
	note.save()
	notes = NoteEntry.objects.all()
	assert len(notes) == 1
	assert notes[0].user == custom_user
	assert notes[0].content == "I have to order 'Eloquent JavaScript'"
	assert isinstance(notes[0].content, str) and notes[0].content is not None
