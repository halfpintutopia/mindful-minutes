import json

from datetime import date
# https://dennisokeeffe.medium.com/mocking-python-datetime-in-tests-with
# -freezegun-f5532307d6d6
from freezegun import freeze_time

from django.urls import reverse

from rest_framework import status

import pytest

from journal.models import AppointmentEntry


# use this to ensure the data is not persisted
@pytest.mark.django_db
def test_list_all_appointments(authenticated_user, add_appointment_entry):
	"""
	GIVEN a Django application
	WHEN the user requests all the appointment entries
	THEN the user should receive a list of all the appointment entries
	"""
	client, user = authenticated_user
	
	add_appointment_entry(
		title="Dentist",
		date=date.today(),
		time_from="09:00:00",
		time_until="10:00:00",
		user=user,
		)
	
	add_appointment_entry(
		title="Gym",
		date=date.today(),
		time_from="19:00:00",
		time_until="20:00:00",
		user=user,
		)
	
	add_appointment_entry(
		title="Lunch with Maria",
		date=date.today(),
		time_from="12:00:00",
		time_until="13:00:00",
		user=user,
		)
	
	add_appointment_entry(
		title="Cinema",
		date=date.today(),
		time_from="19:00:00",
		time_until="22:00:00",
		user=user,
		)
	
	url = reverse(
		"appointment-entry-list-all",
		args=[user.slug]
		)
	
	res = client.get(
		url,
		content_type="application/json"
		)
	
	assert res.status_code == status.HTTP_200_OK
	assert res.data[0]["user"] == user.id
	assert res.data[0]["date"] == date.today().strftime("%Y-%m-%d")


@pytest.mark.django_db
def test_add_appointment_entry(authenticated_user):
	"""
	GIVEN a Django application
	WHEN the user requests to add an appointment entry
	THEN check that the appointment entry is added
	"""
	appointment_entries = AppointmentEntry.objects.all()
	assert len(appointment_entries) == 0
	
	current_date = date.today()
	
	client, user = authenticated_user
	
	appointment_data = {
		"title":      "Dentist",
		"date":       str(current_date),
		"time_from":  "09:00:00",
		"time_until": "10:00:00",
		"user":       user.id,
		}
	
	url = reverse(
		"appointment-entry-list-date",
		args=[user.slug, current_date]
		)
	
	res = client.post(
		url,
		json.dumps(appointment_data),
		content_type="application/json"
		)
	
	assert res.status_code == status.HTTP_201_CREATED
	assert res.data["user"] == user.id
	assert res.data["title"] == "Dentist"
	assert res.data["date"] == str(current_date)
	assert res.data["time_from"] == "09:00:00"
	assert res.data["time_until"] == "10:00:00"
	
	appointment_entries = AppointmentEntry.objects.all()
	assert len(appointment_entries) == 1


@pytest.mark.django_db
@pytest.mark.parametrize(
	"test_data", [
		{
			"payload": {},
			},
		{
			"payload": {
				"title":      "Dentist",
				"time from":  "09:00:00",
				"time until": "10:00:00"
				},
			}
		]
	)
def test_add_appointment_entry_incorrect_json(authenticated_user, test_data):
	"""
	GIVEN a Django application
	WHEN the user requests to add an appointment entry with an invalid payload
	THEN the payload is not sent
	"""
	appointment_entries = AppointmentEntry.objects.all()
	assert len(appointment_entries) == 0
	
	current_date = date.today()
	
	client, user = authenticated_user
	
	test_data["payload"]["date"] = current_date
	test_data["payload"]["user"] = user.id
	
	url = reverse(
		"appointment-entry-list-date",
		args=[user.slug, str(current_date)]
		)
	
	res = client.post(
		url,
		{},
		content_type="application/json"
		)
	assert res.status_code == status.HTTP_400_BAD_REQUEST
	
	appointment_entries = AppointmentEntry.objects.all()
	assert len(appointment_entries) == 0


@pytest.mark.django_db
@pytest.mark.parametrize("date_param", ["2023-07-01", "2023-06-20"])
def test_add_appointment_entry_not_current_date(
		authenticated_user,
		date_param
		):
	"""
	GIVEN a Django application
	WHEN the user attempts to add an appointment entry on a date,
	that is not the current date
	THEN the appointment entry is not created
	"""
	appointment_entries = AppointmentEntry.objects.all()
	assert len(appointment_entries) == 0
	
	current_date = date.today()
	
	client, user = authenticated_user
	
	appointment_data = {
		"title":      "Dentist",
		"date":       current_date,
		"time_from":  "09:00:00",
		"time_until": "10:00:00",
		"user":       user.id,
		}
	
	url = reverse(
		"appointment-entry-list-date",
		args=[user.slug, date_param]
		)
	
	res = client.post(
		url,
		appointment_data,
		content_type="application/json"
		)
	
	assert res.status_code == status.HTTP_403_FORBIDDEN
	
	appointment_entries = AppointmentEntry.objects.all()
	assert len(appointment_entries) == 0


@pytest.mark.django_db
def test_get_single_appointment_entry(
		authenticated_user,
		add_appointment_entry
		):
	"""
	GIVEN a Django application
	WHEN the user requests to retrieve an appointment entry
	THEN check that the appointment entry is retrieved
	"""
	current_date = date.today()
	
	client, user = authenticated_user
	
	appointment_entry = add_appointment_entry(
		title="Dentist",
		date=current_date,
		time_from="09:00:00",
		time_until="10:00:00",
		user=user,
		)
	
	appointment_date = appointment_entry.created_on.strftime("%Y-%m-%d")
	
	url = reverse(
		"appointment-entry-detail-single",
		args=[user.slug, appointment_date, appointment_entry.id]
		)
	
	res = client.get(
		url,
		content_type="application/json"
		)
	
	assert res.status_code == status.HTTP_200_OK
	assert res.data["user"] == user.id
	assert res.data["title"] == "Dentist"
	assert res.data["time_from"] == "09:00:00"
	assert res.data["time_until"] == "10:00:00"


@pytest.mark.django_db
def test_get_single_appointment_entry_incorrect_id(
		authenticated_user,
		):
	"""
	GIVEN a Django application
	WHEN the user requests to retrieve an appointment entry with an
	incorrect id
	THEN check the appointment entry is not retrieved
	"""
	client, user = authenticated_user
	
	current_date = date.today()
	
	invalid_id = 14258
	
	url = reverse(
		"appointment-entry-detail-single",
		args=[user.slug, current_date, invalid_id]
		)
	
	res = client.get(
		url
		)
	
	assert res.status_code == status.HTTP_404_NOT_FOUND


@pytest.mark.django_db
def test_get_all_appointment_entries_by_current_date(
		authenticated_user,
		add_appointment_entry,
		):
	"""
	GIVEN a Django application
	WHEN the user requests to retrieve all appointment entries
	by current date
	THEN check all appointment entries are retrieved
	"""
	appointment_entries = AppointmentEntry.objects.all()
	assert len(appointment_entries) == 0
	
	current_date = date.today()
	
	client, user = authenticated_user
	
	add_appointment_entry(
		title="Dentist",
		date="2023-07-06",
		time_from="09:00:00",
		time_until="10:00:00",
		user=user,
		)
	
	add_appointment_entry(
		title="Gym",
		date="2023-07-06",
		time_from="19:00:00",
		time_until="20:00:00",
		user=user,
		)
	
	add_appointment_entry(
		title="Lunch with Maria",
		date="2023-07-04",
		time_from="12:00:00",
		time_until="13:00:00",
		user=user,
		)
	
	add_appointment_entry(
		title="Cinema",
		date="2023-07-09",
		time_from="19:00:00",
		time_until="22:00:00",
		user=user,
		)
	
	url = reverse(
		"appointment-entry-list-date",
		args=[user.slug, str(current_date)]
		)
	
	res = client.get(
		url
		)
	
	assert res.status_code == status.HTTP_200_OK
	assert res.data[0]["created_on"] == str(current_date)
	
	appointment_entries = AppointmentEntry.objects.filter(
		created_on__date=current_date
		)
	assert len(appointment_entries) == 4


@pytest.mark.django_db
@pytest.mark.parametrize(
	"created_on_timestamp", [
		"2023-07-06 12:00:00",
		"2023-06-04 10:30:00",
		"2022-07-09 19:45:00",
		]
	)
def test_get_all_appointment_entries_by_date(
		authenticated_user,
		add_appointment_entry,
		created_on_timestamp
		):
	"""
	GIVEN a Django application
	WHEN the user requests to retrieve all appointment entries by date
	THEN check all appointment entries are retrieved
	"""
	client, user = authenticated_user
	
	with freeze_time(created_on_timestamp):
		appointment_entries = AppointmentEntry.objects.all()
		assert len(appointment_entries) == 0
		
		current_date = date.today()
		
		add_appointment_entry(
			title="Dentist",
			date="2023-07-06",
			time_from="09:00:00",
			time_until="10:00:00",
			user=user,
			)
		
		add_appointment_entry(
			title="Gym",
			date="2023-07-06",
			time_from="19:00:00",
			time_until="20:00:00",
			user=user,
			)
		
		add_appointment_entry(
			title="Lunch with Maria",
			date="2023-07-04",
			time_from="12:00:00",
			time_until="13:00:00",
			user=user,
			)
		
		add_appointment_entry(
			title="Cinema",
			date="2023-07-09",
			time_from="19:00:00",
			time_until="22:00:00",
			user=user,
			)
	
	url = reverse(
		"appointment-entry-list-date",
		args=[user.slug, current_date]
		)
	
	res = client.get(
		url
		)
	
	assert res.status_code == status.HTTP_200_OK
	assert res.data[0]["created_on"] == str(current_date)
	
	appointment_entries = AppointmentEntry.objects.filter(
		created_on__date=current_date
		)
	assert len(appointment_entries) == 4


@pytest.mark.django_db
def test_remove_appointment_entry(
		authenticated_user,
		add_appointment_entry
		):
	"""
	GIVEN a Django application
	WHEN the user requests to remove an appointment entry
	THEN the appointment entry is removed
	"""
	appointment_entries = AppointmentEntry.objects.all()
	assert len(appointment_entries) == 0
	
	current_date = date.today()
	
	client, user = authenticated_user
	
	appointment_entry = add_appointment_entry(
		title="Dentist",
		date=current_date,
		time_from="09:00:00",
		time_until="10:00:00",
		user=user,
		)
	
	appointment_date = appointment_entry.created_on.strftime("%Y-%m-%d")
	
	url = reverse(
		"appointment-entry-detail-single",
		args=[user.slug, appointment_date, appointment_entry.id]
		)
	
	res = client.get(
		url,
		content_type="application/json"
		)
	
	assert res.status_code == status.HTTP_200_OK
	assert res.data["title"] == "Dentist"
	
	res_delete = client.delete(
		url,
		content_type="application/json"
		)
	
	assert res_delete.status_code == status.HTTP_204_NO_CONTENT
	
	url_retrieve = reverse(
		"appointment-entry-list-date",
		args=[user.slug, appointment_date]
		)
	
	res_retrieve = client.get(
		url_retrieve,
		content_type="application/json"
		)
	
	assert res_retrieve.status_code == status.HTTP_200_OK
	assert len(res_retrieve.data) == 0
	
	assert not AppointmentEntry.objects.filter(
		id=appointment_entry.id
		).exists()
	
	appointment_entries = AppointmentEntry.objects.all()
	assert len(appointment_entries) == 0


@pytest.mark.django_db
def test_remove_appointment_invalid_id(
		authenticated_user
		):
	"""
	GIVEN a Django application
	WHEN the user requests to remove an appointment entry with an invalid id
	THEN the appointment entry is not removed
	"""
	appointment_entries = AppointmentEntry.objects.all()
	assert len(appointment_entries) == 0
	
	current_date = date.today()
	
	invalid_id = 12756
	
	client, user = authenticated_user
	
	url = reverse(
		"appointment-entry-detail-single",
		args=[user.slug, current_date, invalid_id]
		)
	
	res = client.delete(
		url,
		content_type="application/json"
		)
	
	assert res.status_code == status.HTTP_404_NOT_FOUND
	
	updated_appointment_entries = AppointmentEntry.objects.all()
	assert len(appointment_entries) == len(updated_appointment_entries)
	assert len(updated_appointment_entries) == 0


@pytest.mark.django_db
@pytest.mark.parametrize(
	"requested_date", [
		"2024-07-06 19:45:00", "2023-03-05 07:15:00", "2022-09-16 16:20:00"
		]
	)
def test_remove_appointment_not_current_date(
		authenticated_user,
		requested_date,
		add_appointment_entry
		):
	"""
	GIVEN a Django application
	WHEN the user requests to remove an appointment entry when the date is
	not today
	THEN the appointment entry is not removed
	"""
	client, user = authenticated_user
	
	date_and_time = requested_date.split(" ")
	
	with freeze_time(requested_date):
		appointment_entry = add_appointment_entry(
			title="Dentist",
			date=date_and_time[0],
			time_from="09:00:00",
			time_until="10:00:00",
			user=user,
			)
	
	appointment_entries = AppointmentEntry.objects.all()
	assert len(appointment_entries) == 1
	
	url = reverse(
		"appointment-entry-detail-single",
		args=[user.slug, date_and_time[0], appointment_entry.id]
		)
	
	res = client.delete(
		url,
		content_type="application/json"
		)
	
	assert res.status_code == status.HTTP_403_FORBIDDEN
	
	updated_appointment_entries = AppointmentEntry.objects.all()
	assert len(appointment_entries) == len(updated_appointment_entries)
	assert len(updated_appointment_entries) == 1


@pytest.mark.django_db
@pytest.mark.parametrize(
	"test_data", [
		{
			"payload": {
				"title":      "Dentist",
				"time_from":  "10:00:00",
				"time_until": "11:00:00",
				}
			},
		{
			"payload": {
				"title":      "Dentist",
				"time_from":  "14:00:00",
				"time_until": "14:30:00",
				}
			}
		]
	)
def test_update_appointment_entry(
		authenticated_user,
		add_appointment_entry,
		test_data
		):
	"""
	GIVEN a Django application
	WHEN the user requests to update an appointment entry
	THEN the appointment entry is updated
	"""
	appointment_entries = AppointmentEntry.objects.all()
	assert len(appointment_entries) == 0
	
	current_date = date.today()
	
	client, user = authenticated_user
	
	appointment_entry = add_appointment_entry(
		title="Dentist",
		date=str(current_date),
		time_from="09:00:00",
		time_until="10:00:00",
		user=user,
		)
	
	test_data["payload"]["user"] = user.id
	test_data["payload"]["date"] = str(current_date)
	
	url = reverse(
		"appointment-entry-detail-single",
		args=[user.slug, current_date, appointment_entry.id]
		)
	
	res = client.put(
		url,
		json.dumps(test_data["payload"]),
		content_type="application/json"
		)
	
	assert res.status_code == status.HTTP_200_OK
	assert res.data["time_from"] == test_data["payload"]["time_from"]
	assert res.data["time_until"] == test_data["payload"]["time_until"]
	
	res_check = client.get(
		url,
		content_type="application/json"
		)
	
	assert res_check.status_code == status.HTTP_200_OK
	assert res.data["time_from"] == test_data["payload"]["time_from"]
	assert res.data["time_until"] == test_data["payload"]["time_until"]
	
	appointment_entries = AppointmentEntry.objects.all()
	assert len(appointment_entries) == 1


@pytest.mark.django_db
def test_update_appointment_entry_invalid_id(
		authenticated_user
		):
	"""
	GIVEN a Django application
	WHEN the user requests to update an appointment entry with an incorrect id
	THEN the appointment entry is not updated
	"""
	client, user = authenticated_user
	
	current_date = date.today()
	
	invalid_id = 12574
	
	url = reverse(
		"appointment-entry-detail-single",
		args=[user.slug, current_date, invalid_id]
		)
	
	res = client.put(
		url,
		content_type="application/json"
		)
	
	assert res.status_code == status.HTTP_404_NOT_FOUND


@pytest.mark.django_db
@pytest.mark.parametrize(
	"requested_timestamp", [
		"2024-07-06 17:00:00",
		"2023-03-05 23:15:00",
		"2022-09-16 06:30:00"
		]
	)
def test_update_appointment_entry_incorrect_date(
		authenticated_user,
		requested_timestamp,
		add_appointment_entry
		):
	"""
	GIVEN a Django application
	WHEN the user requests to update an appointment entry with an incorrect
	date
	THEN the appointment entry is not and permission denied
	"""
	client, user = authenticated_user
	
	date_and_time = requested_timestamp.split(" ")
	
	with freeze_time(requested_timestamp):
		appointment_entry = add_appointment_entry(
			title="Dentist",
			date=date_and_time[0],
			time_from="09:00:00",
			time_until="10:00:00",
			user=user,
			)
	
	url = reverse(
		"appointment-entry-detail-single",
		args=[user.slug, date_and_time[0], appointment_entry.id]
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
				"title":      "Dentist",
				"date":       "2023-07-06",
				"time from":  "09:00:00",
				"time until": "10:00:00",
				},
			}
		]
	)
def test_update_appointment_entry_invalid_json(
		authenticated_user,
		add_appointment_entry,
		test_data
		):
	"""
	GIVEN a Django application
	WHEN the user requests to update an appointment entry with invalid JSON
	THEN the appointment entry is not updated
	"""
	client, user = authenticated_user
	
	current_date = date.today()
	
	appointment_entry = add_appointment_entry(
		title="Dentist",
		date="2023-07-06",
		time_from="09:00:00",
		time_until="10:00:00",
		user=user,
		)
	
	appointment_date = appointment_entry.created_on.strftime("%Y-%m-%d")
	
	url = reverse(
		"appointment-entry-detail-single",
		args=[user.slug, appointment_date, appointment_entry.id]
		)
	
	res = client.put(
		url,
		json.dumps(test_data["payload"]),
		content_type="application/json"
		)
	
	assert res.status_code == status.HTTP_400_BAD_REQUEST
