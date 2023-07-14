import pytest

from journal.models import KnowledgeEntry


@pytest.mark.django_db
def test_create_knowledge_entry(custom_user):
	"""
	GIVEN a knowledge entry model
	WHEN creating a knowledge entry
	THEN user should have successfully created a knowledge entry
	"""
	knowledge_entry = KnowledgeEntry.objects.create(
		user=custom_user,
		content="Understand what 'hoisting' means in JavaScript",
		)
	knowledge_entry.save()
	knowledge_entries = KnowledgeEntry.objects.all()
	assert len(knowledge_entries) == 1
	assert knowledge_entries[0].user == custom_user
	assert (knowledge_entries[0].content ==
	        "Understand what 'hoisting' means in JavaScript")
	assert isinstance(
		knowledge_entries[0].content, str
		) and knowledge_entries[0].content is not None
