import json
from datetime import date
# https://dennisokeeffe.medium.com/mocking-python-datetime-in-tests-with
# -freezegun-f5532307d6d6
from freezegun import freeze_time

from django.urls import reverse

from rest_framework import status

import pytest

from journal.models import WinEntry


@pytest.mark.django_db
def test_get_list_of_win_entries(authenticated_user, add_win_entry):
	"""
	GIVEN a Django application
	WHEN a user requests a list of all win entries
	THEN the user should receive a list of all win entries
	"""
	client, user = authenticated_user
	
	win_entries = [
		'Meditated for 45 minutes',
		'Handed in my last project',
		'Did hot yoga',
		'Did the Hackathon in Zurich'
		]
	
	for win in win_entries:
		add_win_entry(
			user=user,
			title=win,
			)
	
	url = reverse(
		"win-entry-list-all",
		args=[user.slug]
		)
	
	res = client.get(
		url
		)
	
	assert res.status_code == status.HTTP_200_OK


@pytest.mark.django_db
def test_add_win_entry(authenticated_user):
	"""
	GIVEN a Django application
	WHEN the user requests to add an win entry
	THEN check that the win entry is added
	"""
	win_entries = WinEntry.objects.all()
	assert len(win_entries) == 0
	
	current_date = date.today()
	
	client, user = authenticated_user
	
	win_data = {
		"title": "Finished HTML and CSS",
		"user":  user.id,
		}
	
	url = reverse(
		"win-entry-list-date",
		args=[user.slug, current_date]
		)
	
	res = client.post(
		url,
		json.dumps(win_data),
		content_type="application/json"
		)
	
	assert res.status_code == status.HTTP_201_CREATED
	assert res.data["user"] == user.id
	assert res.data["title"] == "Finished HTML and CSS"
	
	win_entries = WinEntry.objects.all()
	assert len(win_entries) == 1


@pytest.mark.django_db
@pytest.mark.parametrize(
	"test_data", [
		{
			"payload": {},
			},
		{
			"payload": {
				"title entry": "Finished HTML and CSS",
				},
			}
		]
	)
def test_add_win_entry_incorrect_json(authenticated_user, test_data):
	"""
	GIVEN a Django application
	WHEN the user requests to add an win entry with an invalid payload
	THEN the payload is not sent
	"""
	win_entries = WinEntry.objects.all()
	assert len(win_entries) == 0
	
	current_date = date.today()
	
	client, user = authenticated_user
	
	test_data["payload"]["user"] = user.id
	
	url = reverse(
		"win-entry-list-date",
		args=[user.slug, current_date]
		)
	
	res = client.post(
		url,
		json.dumps(test_data["payload"]),
		content_type="application/json"
		)
	assert res.status_code == status.HTTP_400_BAD_REQUEST
	
	win_entries = WinEntry.objects.all()
	assert len(win_entries) == 0


@pytest.mark.django_db
@pytest.mark.parametrize("date_param", ["2023-07-01", "2023-06-20"])
def test_add_win_entry_not_current_date(
		authenticated_user,
		date_param
		):
	"""
	GIVEN a Django application
	WHEN the user attempts to add an win entry on a date,
	that is not the current date
	THEN the win entry is not created
	"""
	win_entries = WinEntry.objects.all()
	assert len(win_entries) == 0
	
	client, user = authenticated_user
	
	win_data = {
		"title": "Finished HTML and CSS",
		"user":  user.id,
		}
	
	url = reverse(
		"win-entry-list-date",
		args=[user.slug, date_param]
		)
	
	res = client.post(
		url,
		win_data,
		content_type="application/json"
		)
	
	assert res.status_code == status.HTTP_403_FORBIDDEN
	
	win_entries = WinEntry.objects.all()
	assert len(win_entries) == 0


@pytest.mark.django_db
def test_get_single_win_entry(
		authenticated_user,
		add_win_entry
		):
	"""
	GIVEN a Django application
	WHEN the user requests to retrieve an win entry
	THEN check that the win entry is retrieved
	"""
	current_date = date.today()
	
	client, user = authenticated_user
	
	win_entry = add_win_entry(
		title="Finished HTML and CSS",
		user=user,
		)
	
	url = reverse(
		"win-entry-detail-single",
		args=[user.slug, current_date, win_entry.id]
		)
	
	res = client.get(
		url,
		content_type="application/json"
		)
	
	assert res.status_code == status.HTTP_200_OK
	assert res.data["user"] == user.id
	assert res.data["title"] == "Finished HTML and CSS"


@pytest.mark.django_db
def test_get_single_win_entry_incorrect_id(
		authenticated_user,
		):
	"""
	GIVEN a Django application
	WHEN the user requests to retrieve an win entry with an incorrect id
	THEN check the win entry is not retrieved
	"""
	client, user = authenticated_user
	
	current_date = date.today()
	invalid_id = 14258
	
	url = reverse(
		"win-entry-detail-single",
		args=[user.slug, current_date, invalid_id]
		)
	
	res = client.get(url)
	
	assert res.status_code == status.HTTP_404_NOT_FOUND


@pytest.mark.django_db
def test_get_all_win_entries_by_current_date(
		authenticated_user,
		add_win_entry
		):
	"""
	GIVEN a Django application
	WHEN the user requests to retrieve all win entries
	by current date
	THEN check all win entries are retrieved
	"""
	win_entries = WinEntry.objects.all()
	assert len(win_entries) == 0
	
	current_date = date.today()
	
	client, user = authenticated_user
	
	add_win_entry(
		title="Finished HTML and CSS",
		user=user,
		)
	
	add_win_entry(
		title="Had a conversation in German",
		user=user,
		)
	
	add_win_entry(
		title="Hiked for 20 kms",
		user=user,
		)
	
	add_win_entry(
		title="Read 30 pages of Momo in German",
		user=user,
		)
	
	url = reverse(
		"win-entry-list-date",
		args=[user.slug, current_date]
		)
	
	res = client.get(url)
	
	assert res.status_code == status.HTTP_200_OK
	assert res.data[0]["created_on"] == str(current_date)
	
	win_entries = WinEntry.objects.filter(
		created_on__date=current_date
		)
	assert len(win_entries) == 4


@pytest.mark.django_db
@pytest.mark.parametrize(
	"created_on_timestamp", [
		"2023-07-06 12:00:00",
		"2023-06-04 10:30:00",
		"2022-07-09 19:45:00",
		]
	)
def test_get_all_win_entries_by_date(
		authenticated_user,
		add_win_entry,
		created_on_timestamp
		):
	"""
	GIVEN a Django application
	WHEN the user requests to retrieve all win entries by date
	THEN check all win entries are retrieved
	"""
	date_and_time = created_on_timestamp.split(" ")
	client, user = authenticated_user
	
	with freeze_time(created_on_timestamp):
		win_entries = WinEntry.objects.all()
		assert len(win_entries) == 0
		
		add_win_entry(
			title="Finished HTML and CSS",
			user=user,
			)
		
		add_win_entry(
			title="Had a conversation in German",
			user=user,
			)
		
		add_win_entry(
			title="Hiked for 20 kms",
			user=user,
			)
		
		add_win_entry(
			title="Read 30 pages of Momo in German",
			user=user,
			)
	
	url = reverse(
		"win-entry-list-date",
		args=[user.slug, date_and_time[0]]
		)
	res = client.get(url)
	
	assert res.status_code == status.HTTP_200_OK
	assert res.data[0]["created_on"] == date_and_time[0]
	
	win_entries = WinEntry.objects.filter(
		created_on__date=date_and_time[0]
		)
	assert len(win_entries) == 4


@pytest.mark.django_db
def test_remove_win_entry(
		authenticated_user,
		add_win_entry
		):
	"""
	GIVEN a Django application
	WHEN the user requests to remove an win entry
	THEN the win entry is removed
	"""
	win_entries = WinEntry.objects.all()
	assert len(win_entries) == 0
	
	client, user = authenticated_user
	
	win_entry = add_win_entry(
		title="Finished HTML and CSS",
		user=user,
		)
	
	win_date = win_entry.created_on.strftime("%Y-%m-%d")
	
	url = reverse(
		"win-entry-detail-single",
		args=[user.slug, win_date, win_entry.id]
		)
	
	res = client.get(
		url,
		content_type="application/json"
		)
	
	assert res.status_code == status.HTTP_200_OK
	assert res.data["title"] == "Finished HTML and CSS"
	
	res_delete = client.delete(
		url,
		content_type="application/json"
		)
	
	assert res_delete.status_code == status.HTTP_204_NO_CONTENT
	
	url_retrieve = reverse(
		"win-entry-list-date",
		args=[user.slug, win_date]
		)
	
	res_retrieve = client.get(
		url_retrieve,
		content_type="application/json"
		)
	
	assert res_retrieve.status_code == status.HTTP_200_OK
	assert len(res_retrieve.data) == 0
	
	assert not WinEntry.objects.filter(id=win_entry.id).exists()
	
	win_entries = WinEntry.objects.all()
	assert len(win_entries) == 0


@pytest.mark.django_db
def test_remove_win_invalid_id(
		authenticated_user
		):
	"""
	GIVEN a Django application
	WHEN the user requests to remove an win entry with an invalid id
	THEN the win entry is not removed
	"""
	win_entries = WinEntry.objects.all()
	assert len(win_entries) == 0
	
	current_date = date.today()
	invalid_id = 12756
	
	client, user = authenticated_user
	
	url = reverse(
		"win-entry-detail-single",
		args=[user.slug, current_date, invalid_id]
		)
	
	res = client.delete(
		url,
		content_type="application/json"
		)
	
	assert res.status_code == status.HTTP_404_NOT_FOUND
	
	updated_win_entries = WinEntry.objects.all()
	assert len(win_entries) == len(updated_win_entries)
	assert len(updated_win_entries) == 0


@pytest.mark.django_db
@pytest.mark.parametrize(
	"requested_date", [
		"2024-07-06 12:00:00",
		"2023-03-05 15:30:00",
		"2022-09-16 23:15:00"
		]
	)
def test_remove_win_not_current_date(
		authenticated_user, requested_date, add_win_entry
		):
	"""
	GIVEN a Django application
	WHEN the user requests to remove an win entry when the date is not today
	THEN the win entry is not removed
	"""
	win_entries = WinEntry.objects.all()
	assert len(win_entries) == 0
	
	client, user = authenticated_user
	date_and_time = requested_date.split(" ")
	
	with freeze_time(requested_date):
		win_entry = add_win_entry(
			title="Finished HTML and CSS",
			user=user,
			)
	
	url = reverse(
		"win-entry-detail-single",
		args=[user.slug, date_and_time[0], win_entry.id]
		)
	
	res = client.delete(
		url,
		content_type="application/json"
		)
	
	assert res.status_code == status.HTTP_403_FORBIDDEN
	
	updated_win_entries = WinEntry.objects.all()
	assert len(updated_win_entries) == 1


@pytest.mark.django_db
@pytest.mark.parametrize(
	"test_data", [
		{
			"payload": {
				"title": "Finished HTML and CSS",
				}
			},
		{
			"payload": {
				"title": "Had a conversation in German",
				}
			},
		{
			"payload": {
				"title": "Hiked for 20 kms",
				}
			}
		]
	)
def test_update_win_entry(
		authenticated_user,
		add_win_entry,
		test_data
		):
	"""
	GIVEN a Django application
	WHEN the user requests to update an win entry
	THEN the win entry is updated
	"""
	win_entries = WinEntry.objects.all()
	assert len(win_entries) == 0
	
	current_date = date.today()
	
	client, user = authenticated_user
	
	win_entry = add_win_entry(
		title="Finished HTML and CSS",
		user=user,
		)
	
	test_data["payload"]["user"] = user.id
	
	url = reverse(
		"win-entry-detail-single",
		args=[user.slug, current_date, win_entry.id]
		)
	
	res = client.put(
		url,
		json.dumps(test_data["payload"]),
		content_type="application/json"
		)
	
	assert res.status_code == status.HTTP_200_OK
	assert res.data["title"] == test_data["payload"]["title"]
	
	res_check = client.get(
		url,
		content_type="application/json"
		)
	
	assert res_check.status_code == status.HTTP_200_OK
	assert res.data["title"] == test_data["payload"]["title"]
	
	win_entries = WinEntry.objects.all()
	assert len(win_entries) == 1


@pytest.mark.django_db
def test_update_win_entry_incorrect_data(
		authenticated_user,
		add_win_entry
		):
	"""
	GIVEN a Django application
	WHEN the user requests to update an win entry with an incorrect id
	THEN the win entry is not updated
	"""
	client, user = authenticated_user
	
	current_date = date.today()
	invalid_id = 12574
	
	add_win_entry(
		title="Finished HTML and CSS",
		user=user,
		)
	
	win_data = {
		"title": "Finished HTML and CSS",
		"user":  user.id,
		}
	
	url = reverse(
		"win-entry-detail-single",
		args=[user.slug, current_date, invalid_id]
		)
	
	res = client.put(
		url,
		json.dumps(win_data),
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
def test_update_win_entry_incorrect_date(
		authenticated_user,
		requested_date,
		add_win_entry
		):
	"""
	GIVEN a Django application
	WHEN the user requests to update an win entry with an incorrect date
	THEN the win entry is not and permission denied
	"""
	date_and_time = requested_date.split(" ")
	
	client, user = authenticated_user
	
	with freeze_time(requested_date):
		win_entry = add_win_entry(
			title="Finished HTML and CSS",
			user=user,
			)
	
	url = reverse(
		"win-entry-detail-single",
		args=[user.slug, date_and_time[0], win_entry.id]
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
				"title input": "Finished HTML and CSS",
				},
			}
		]
	)
def test_update_win_entry_invalid_json(
		authenticated_user,
		add_win_entry,
		test_data
		):
	"""
	GIVEN a Django application
	WHEN the user requests to update an win entry with invalid JSON
	THEN the win entry is not updated
	"""
	client, user = authenticated_user
	
	current_date = date.today()
	
	win_entry = add_win_entry(
		title="Dentist",
		user=user,
		)
	
	url = reverse(
		"win-entry-detail-single",
		args=[user.slug, current_date, win_entry.id]
		)
	
	res = client.put(
		url,
		test_data["payload"],
		content_type="application/json"
		)
	
	assert res.status_code == status.HTTP_400_BAD_REQUEST
