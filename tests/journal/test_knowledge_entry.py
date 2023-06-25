import pytest

from django.contrib.auth import get_user_model

from journal.models import KnowledgeEntry

User = get_user_model()


@pytest.fixture
def user():
    """
    Fixture for creating a user object
    """
    return User.objects.create_user(
        email="normal@user.com",
        password="abcdefghij123!+_",
        first_name="Normal",
        last_name="User"
    )


@pytest.mark.django_db
def test_create_knowledge_entry(user):
    """
    GIVEN a knowledge entry model
    WHEN creating a knowledge entry
    THEN user should have successfully created a knowledge entry
    """
    knowledge_entry = KnowledgeEntry.objects.create(
        user=user,
        content="Understand what 'hoisting' means in JavaScript",
    )
    knowledge_entry.save()
    knowledge_entries = KnowledgeEntry.objects.all()
    assert len(knowledge_entries) == 1
    assert knowledge_entries[0].user == user
    assert (knowledge_entries[0].content ==
            "Understand what 'hoisting' means in JavaScript")
    assert isinstance(
        knowledge_entries[0].content, str
    ) and knowledge_entries[0].content is not None
