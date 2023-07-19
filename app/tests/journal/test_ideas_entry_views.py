import json
from datetime import date
# https://dennisokeeffe.medium.com/mocking-python-datetime-in-tests-with
# -freezegun-f5532307d6d6
from freezegun import freeze_time

from django.urls import reverse

from rest_framework import status

import pytest

from journal.models import IdeasEntry


@pytest.mark.django_db
def test_get_list_of_ideas_entries(authenticated_user, add_ideas_entry):
	"""
	GIVEN a Django application
	WHEN a user requests a list of all ideas entries
	THEN the user should receive a list of all ideas entries
	"""
	client, user = authenticated_user
	
	ideas = [
		'Learn more about canvas.',
		'Can I create a game with just CSS?',
		'Pet Adoption for next project?',
		'Learn more about Vue',
		'Create a React project include GraphQL',
		]
	
	for idea in ideas:
		add_ideas_entry(
			user=user,
			content=idea
			)
	
	url = reverse(
		"ideas-entry-list-all",
		args=[user.slug]
		)
	
	res = client.get(
		url
		)
	
	assert res.status_code == status.HTTP_200_OK


@pytest.mark.django_db
def test_add_ideas_entry(authenticated_user):
	"""
	GIVEN a Django application
	WHEN the user requests to add an ideas entry
	THEN check that the ideas entry is added
	"""
	ideas_entries = IdeasEntry.objects.all()
	assert len(ideas_entries) == 0
	
	current_date = date.today()
	
	client, user = authenticated_user
	
	ideas_data = {
		"content": "Check out TypeScript course on Frontend Masters.",
		"user":    user.id,
		}
	
	url = reverse(
		"ideas-entry-list-date",
		args=[user.slug, current_date]
		)
	
	res = client.post(
		url,
		json.dumps(ideas_data),
		content_type="application/json"
		)
	
	assert res.status_code == status.HTTP_201_CREATED
	assert res.data["user"] == user.id
	assert res.data[
		       "content"] == "Check out TypeScript course on Frontend " \
                             "Masters."
	
	ideas_entries = IdeasEntry.objects.all()
	assert len(ideas_entries) == 1


@pytest.mark.django_db
@pytest.mark.parametrize(
	"test_data", [
		{
			"payload":     {},
			"status_code": 400
			},
		{
			"payload":     {
				"content entry": "Check out TypeScript course on Frontend "
                                 "Masters.",
				},
			"status_code": 400
			}
		]
	)
def test_add_ideas_entry_incorrect_json(authenticated_user, test_data):
	"""
	GIVEN a Django application
	WHEN the user requests to add an ideas entry with an invalid payload
	THEN the payload is not sent
	"""
	ideas_entries = IdeasEntry.objects.all()
	assert len(ideas_entries) == 0
	
	current_date = date.today()
	
	client, user = authenticated_user
	
	test_data["payload"]["user"] = user.id
	
	url = reverse(
		"ideas-entry-list-date",
		args=[user.slug, current_date]
		)
	
	res = client.post(
		url,
		json.dumps(test_data["payload"]),
		content_type="application/json"
		)
	assert res.status_code == status.HTTP_400_BAD_REQUEST
	
	ideas_entries = IdeasEntry.objects.all()
	assert len(ideas_entries) == 0


@pytest.mark.django_db
@pytest.mark.parametrize("date_param", ["2023-07-01", "2023-06-20"])
def test_add_ideas_entry_not_current_date(
		authenticated_user,
		date_param
		):
	"""
	GIVEN a Django application
	WHEN the user attempts to add an ideas entry on a date,
	that is not the current date
	THEN the ideas entry is not created
	"""
	ideas_entries = IdeasEntry.objects.all()
	assert len(ideas_entries) == 0
	
	client, user = authenticated_user
	
	ideas_data = {
		"content": "Check out TypeScript course on Frontend Masters.",
		"user":    user.id,
		}
	
	url = reverse(
		"ideas-entry-list-date",
		args=[user.slug, date_param]
		)
	
	res = client.post(
		url,
		ideas_data,
		content_type="application/json"
		)
	
	assert res.status_code == status.HTTP_403_FORBIDDEN
	
	ideas_entries = IdeasEntry.objects.all()
	assert len(ideas_entries) == 0


@pytest.mark.django_db
def test_get_single_ideas_entry(
		authenticated_user,
		add_ideas_entry
		):
	"""
	GIVEN a Django application
	WHEN the user requests to retrieve an ideas entry
	THEN check that the ideas entry is retrieved
	"""
	current_date = date.today()
	
	client, user = authenticated_user
	
	ideas_entry = add_ideas_entry(
		content="Check out TypeScript course on Frontend Masters.",
		user=user,
		)
	
	url = reverse(
		"ideas-entry-detail-single",
		args=[user.slug, current_date, ideas_entry.id]
		)
	
	res = client.get(
		url,
		content_type="application/json"
		)
	
	assert res.status_code == status.HTTP_200_OK
	assert res.data["user"] == user.id
	assert res.data[
		       "content"] == "Check out TypeScript course on Frontend " \
                             "Masters."


@pytest.mark.django_db
def test_get_single_ideas_entry_incorrect_id(
		authenticated_user,
		):
	"""
	GIVEN a Django application
	WHEN the user requests to retrieve an ideas entry with an incorrect id
	THEN check the ideas entry is not retrieved
	"""
	client, user = authenticated_user
	
	current_date = date.today()
	invalid_id = 14258
	
	url = reverse(
		"ideas-entry-detail-single",
		args=[user.slug, current_date, invalid_id]
		)
	
	res = client.get(url)
	
	assert res.status_code == status.HTTP_404_NOT_FOUND


@pytest.mark.django_db
def test_get_all_ideas_entries_by_current_date(
		authenticated_user,
		add_ideas_entry
		):
	"""
	GIVEN a Django application
	WHEN the user requests to retrieve all ideas entries
	by current date
	THEN check all ideas entries are retrieved
	"""
	ideas_entries = IdeasEntry.objects.all()
	assert len(ideas_entries) == 0
	
	current_date = date.today()
	
	client, user = authenticated_user
	
	add_ideas_entry(
		content="Check out TypeScript course on Frontend Masters.",
		user=user,
		)
	
	url = reverse(
		"ideas-entry-list-date",
		args=[user.slug, current_date]
		)
	
	res = client.get(url)
	
	assert res.status_code == status.HTTP_200_OK
	assert res.data[0]["created_on"] == str(current_date)
	
	ideas_entries = IdeasEntry.objects.filter(
		created_on__date=current_date
		)
	assert len(ideas_entries) == 1


@pytest.mark.django_db
@pytest.mark.parametrize(
	"created_on_timestamp", [
		"2023-07-06 12:00:00",
		"2023-06-04 10:30:00",
		"2022-07-09 19:45:00",
		]
	)
def test_get_all_ideas_entries_by_date(
		authenticated_user,
		add_ideas_entry,
		created_on_timestamp
		):
	"""
	GIVEN a Django application
	WHEN the user requests to retrieve all ideas entries by date
	THEN check all ideas entries are retrieved
	"""
	date_and_time = created_on_timestamp.split(" ")
	client, user = authenticated_user
	
	with freeze_time(created_on_timestamp):
		ideas_entries = IdeasEntry.objects.all()
		assert len(ideas_entries) == 0
		
		add_ideas_entry(
			content="Check out TypeScript course on Frontend Masters.",
			user=user,
			)
	
	url = reverse(
		"ideas-entry-list-date",
		args=[user.slug, date_and_time[0]]
		)
	res = client.get(url)
	
	assert res.status_code == status.HTTP_200_OK
	assert res.data[0]["created_on"] == date_and_time[0]
	
	ideas_entries = IdeasEntry.objects.filter(
		created_on__date=date_and_time[0]
		)
	assert len(ideas_entries) == 1


@pytest.mark.django_db
def test_remove_ideas_entry(
		authenticated_user,
		add_ideas_entry
		):
	"""
	GIVEN a Django application
	WHEN the user requests to remove an ideas entry
	THEN the ideas entry is removed
	"""
	ideas_entries = IdeasEntry.objects.all()
	assert len(ideas_entries) == 0
	
	client, user = authenticated_user
	
	ideas_entry = add_ideas_entry(
		content="Check out TypeScript course on Frontend Masters.",
		user=user,
		)
	
	ideas_date = ideas_entry.created_on.strftime("%Y-%m-%d")
	
	url = reverse(
		"ideas-entry-detail-single",
		args=[user.slug, ideas_date, ideas_entry.id]
		)
	
	res = client.get(
		url,
		content_type="application/json"
		)
	
	assert res.status_code == status.HTTP_200_OK
	assert res.data[
		       "content"] == "Check out TypeScript course on Frontend " \
                             "Masters."
	
	res_delete = client.delete(
		url,
		content_type="application/json"
		)
	
	assert res_delete.status_code == status.HTTP_204_NO_CONTENT
	
	url_retrieve = reverse(
		"ideas-entry-list-date",
		args=[user.slug, ideas_date]
		)
	
	res_retrieve = client.get(
		url_retrieve,
		content_type="application/json"
		)
	
	assert res_retrieve.status_code == status.HTTP_200_OK
	assert len(res_retrieve.data) == 0
	
	assert not IdeasEntry.objects.filter(id=ideas_entry.id).exists()
	
	ideas_entries = IdeasEntry.objects.all()
	assert len(ideas_entries) == 0


@pytest.mark.django_db
def test_remove_ideas_invalid_id(
		authenticated_user
		):
	"""
	GIVEN a Django application
	WHEN the user requests to remove an ideas entry with an invalid id
	THEN the ideas entry is not removed
	"""
	ideas_entries = IdeasEntry.objects.all()
	assert len(ideas_entries) == 0
	
	current_date = date.today()
	invalid_id = 12756
	
	client, user = authenticated_user
	
	url = reverse(
		"ideas-entry-detail-single",
		args=[user.slug, current_date, invalid_id]
		)
	
	res = client.delete(
		url,
		content_type="application/json"
		)
	
	assert res.status_code == status.HTTP_404_NOT_FOUND
	
	updated_ideas_entries = IdeasEntry.objects.all()
	assert len(ideas_entries) == len(updated_ideas_entries)
	assert len(updated_ideas_entries) == 0


@pytest.mark.django_db
@pytest.mark.parametrize(
	"requested_date", [
		"2024-07-06 12:00:00",
		"2023-03-05 15:30:00",
		"2022-09-16 23:15:00"
		]
	)
def test_remove_ideas_not_current_date(
		authenticated_user, requested_date, add_ideas_entry
		):
	"""
	GIVEN a Django application
	WHEN the user requests to remove an ideas entry when the date is not today
	THEN the ideas entry is not removed
	"""
	ideas_entries = IdeasEntry.objects.all()
	assert len(ideas_entries) == 0
	
	client, user = authenticated_user
	date_and_time = requested_date.split(" ")
	current_date = date.today()
	
	with freeze_time(requested_date):
		ideas_entry = add_ideas_entry(
			content="Check out TypeScript course on Frontend Masters.",
			user=user,
			)
	
	url = reverse(
		"ideas-entry-detail-single",
		args=[user.slug, date_and_time[0], ideas_entry.id]
		)
	
	res = client.delete(
		url,
		content_type="application/json"
		)
	
	assert res.status_code == status.HTTP_403_FORBIDDEN
	
	updated_ideas_entries = IdeasEntry.objects.all()
	assert len(updated_ideas_entries) == 1


@pytest.mark.django_db
@pytest.mark.parametrize(
	"test_data", [
		{
			"payload": {
				"content": "Check out TypeScript course on Frontend Masters. "
                           "Refactored code with new ideas.",
				}
			},
		{
			"payload": {
				"content": "Checkout Neo4J Playground.",
				}
			}
		]
	)
def test_update_ideas_entry(
		authenticated_user,
		add_ideas_entry,
		test_data
		):
	"""
	GIVEN a Django application
	WHEN the user requests to update an ideas entry
	THEN the ideas entry is updated
	"""
	ideas_entries = IdeasEntry.objects.all()
	assert len(ideas_entries) == 0
	
	current_date = date.today()
	
	client, user = authenticated_user
	
	ideas_entry = add_ideas_entry(
		content="Check out TypeScript course on Frontend Masters.",
		user=user,
		)
	
	test_data["payload"]["user"] = user.id
	
	url = reverse(
		"ideas-entry-detail-single",
		args=[user.slug, current_date, ideas_entry.id]
		)
	
	res = client.put(
		url,
		json.dumps(test_data["payload"]),
		content_type="application/json"
		)
	
	assert res.status_code == status.HTTP_200_OK
	assert res.data["content"] == test_data["payload"]["content"]
	
	res_check = client.get(
		url,
		content_type="application/json"
		)
	
	assert res_check.status_code == status.HTTP_200_OK
	assert res.data["content"] == test_data["payload"]["content"]
	
	ideas_entries = IdeasEntry.objects.all()
	assert len(ideas_entries) == 1


@pytest.mark.django_db
def test_update_ideas_entry_incorrect_data(
		authenticated_user,
		add_ideas_entry
		):
	"""
	GIVEN a Django application
	WHEN the user requests to update an ideas entry with an incorrect id
	THEN the ideas entry is not updated
	"""
	client, user = authenticated_user
	
	current_date = date.today()
	invalid_id = 12574
	
	add_ideas_entry(
		content="Check out TypeScript course on Frontend Masters.",
		user=user,
		)
	
	ideas_data = {
		"content": "Checkout Neo4J Playground.",
		"user":    user.id,
		}
	
	url = reverse(
		"ideas-entry-detail-single",
		args=[user.slug, current_date, invalid_id]
		)
	
	res = client.put(
		url,
		json.dumps(ideas_data),
		content_type="application/json"
		)
	
	assert res.status_code == status.HTTP_404_NOT_FOUND


@pytest.mark.django_db
@pytest.mark.parametrize(
	"requested_date", [
		"2024-07-01 12:00:00",
		"2023-03-05 06:00:00",
		"2022-09-16 21:15:00"
		]
	)
def test_update_ideas_entry_incorrect_date(
		authenticated_user,
		requested_date,
		add_ideas_entry
		):
	"""
	GIVEN a Django application
	WHEN the user requests to update an ideas entry with an incorrect date
	THEN the ideas entry is not and permission denied
	"""
	date_and_time = requested_date.split(" ")
	
	client, user = authenticated_user
	
	with freeze_time(requested_date):
		ideas_entry = add_ideas_entry(
			content="Check out TypeScript course on Frontend Masters.",
			user=user,
			)
	
	url = reverse(
		"ideas-entry-detail-single",
		args=[user.slug, date_and_time[0], ideas_entry.id]
		)
	
	res = client.put(
		url,
		content_type="application/json"
		)
	
	assert res.status_code == status.HTTP_403_FORBIDDEN


@pytest.mark.django_db
@pytest.mark.parametrize(
	"test_data", [
		{
			"payload": {},
			},
		{
			"payload": {
				"content entry": "Check out TypeScript course on Frontend "
                                 "Masters.",
				},
			}
		]
	)
def test_update_ideas_entry_invalid_json(
		authenticated_user,
		add_ideas_entry,
		test_data
		):
	"""
	GIVEN a Django application
	WHEN the user requests to update an ideas entry with invalid JSON
	THEN the ideas entry is not updated
	"""
	client, user = authenticated_user
	
	current_date = date.today()
	
	ideas_entry = add_ideas_entry(
		content="Dentist",
		user=user,
		)
	
	url = reverse(
		"ideas-entry-detail-single",
		args=[user.slug, current_date, ideas_entry.id]
		)
	
	res = client.put(
		url,
		test_data["payload"],
		content_type="application/json"
		)
	
	assert res.status_code == status.HTTP_400_BAD_REQUEST
