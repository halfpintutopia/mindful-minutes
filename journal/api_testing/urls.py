from django.urls import path

from ..api_views.appointment_entries import AppointmentEntryList, \
	AppointmentEntryDetail, AppointmentEntryListCreate
from ..api_views.target_entries import TargetEntryList, TargetEntryDetail
from ..api_views.note_entries import NoteEntryList, NoteEntryDetail
from ..api_views.knowledge_entries import KnowledgeEntryList, \
	KnowledgeEntryDetail
from ..api_views.gratitude_entries import GratitudeEntryList, \
	GratitudeEntryDetail
from ..api_views.win_entries import WinEntryList, WinEntryDetail
from ..api_views.ideas_entries import IdeasEntryList, IdeasEntryDetail
from ..api_views.improvement_entries import ImprovementEntryList, \
	ImprovementEntryDetail
from ..api_views.custom_user import CustomUserList, CustomUserDetail
from ..api_views.user_settings import UserSettingsView
from ..api_views.emotion_entries import EmotionEntryList, \
	EmotionEntryDetail

urlpatterns = [
	path(
		"api/users/<str:slug>/",
		CustomUserDetail.as_view(),
		name="user-detail"
		),
	path(
		"api/users/",
		CustomUserList.as_view(),
		name="user-list"
		),
	path(
		"api/users/<str:slug>/user-settings/",
		UserSettingsView.as_view(),
		name="user-settings"
		),
	path(
		'api/users/<str:slug>/appointments/',
		AppointmentEntryList.as_view(),
		name='appointment-entry-list'
		),
	path(
		"api/users/<str:slug>/appointments/<str:date_request>/",
		AppointmentEntryListCreate.as_view(),
		name="appointment-entry-date-list"
		),
	path(
		"api/users/<str:slug>/appointments/<str:date_request>/<int:pk>/",
		AppointmentEntryDetail.as_view(),
		name="appointment-entry-detail"
		),
	path(
		"api/users/<str:slug>/target/",
		TargetEntryList.as_view(),
		name="target-entry-list-all"
		),
	path(
		"api/users/<str:slug>/target/<str:date_request>/<int:pk>/",
		TargetEntryDetail.as_view(),
		name="target-entry-detail-single"
		),
	path(
		"api/users/<str:slug>/target/<str:date_request>/",
		TargetEntryList.as_view(),
		name="target-entry-list-date"
		),
	path(
		"api/users/<str:slug>/note/",
		NoteEntryList.as_view(),
		name="note-entry-list-all"
		),
	path(
		"api/users/<str:slug>/note/<str:date_request>/<int:pk>/",
		NoteEntryDetail.as_view(),
		name="note-entry-detail-single"
		),
	path(
		"api/users/<str:slug>/note/<str:date_request>/",
		NoteEntryList.as_view(),
		name="note-entry-list-date"
		),
	path(
		"api/users/<str:slug>/knowledge/",
		KnowledgeEntryList.as_view(),
		name="knowledge-entry-list-all"
		),
	path(
		"api/users/<str:slug>/knowledge/<str:date_request>/<int:pk>/",
		KnowledgeEntryDetail.as_view(),
		name="knowledge-entry-detail-single"
		),
	path(
		"api/users/<str:slug>/knowledge/<str:date_request>/",
		KnowledgeEntryList.as_view(),
		name="knowledge-entry-list-date"
		),
	path(
		"api/users/<str:slug>/gratitude/",
		GratitudeEntryList.as_view(),
		name="gratitude-entry-list-all"
		),
	path(
		"api/users/<str:slug>/gratitude/<str:date_request>/<int:pk>/",
		GratitudeEntryDetail.as_view(),
		name="gratitude-entry-detail-single"
		),
	path(
		"api/users/<str:slug>/gratitude/<str:date_request>/",
		GratitudeEntryList.as_view(),
		name="gratitude-entry-list-date"
		),
	path(
		"api/users/<str:slug>/win/",
		WinEntryList.as_view(),
		name="win-entry-list-all"
		),
	path(
		"api/users/<str:slug>/win/<str:date_request>/<int:pk>/",
		WinEntryDetail.as_view(),
		name="win-entry-detail-single"
		),
	path(
		"api/users/<str:slug>/win/<str:date_request>/",
		WinEntryList.as_view(),
		name="win-entry-list-date"
		),
	path(
		"api/users/<str:slug>/ideas/",
		IdeasEntryList.as_view(),
		name="ideas-entry-list-all"
		),
	path(
		"api/users/<str:slug>/ideas/<str:date_request>/<int:pk>/",
		IdeasEntryDetail.as_view(),
		name="ideas-entry-detail-single"
		),
	path(
		"api/users/<str:slug>/ideas/<str:date_request>/",
		IdeasEntryList.as_view(),
		name="ideas-entry-list-date"
		),
	path(
		"api/users/<str:slug>/improvement/",
		ImprovementEntryList.as_view(),
		name="improvement-entry-list-all"
		),
	path(
		"api/users/<str:slug>/improvement/<str:date_request>/<int:pk>/",
		ImprovementEntryDetail.as_view(),
		name="improvement-entry-detail-single"
		),
	path(
		"api/users/<str:slug>/improvement/<str:date_request>/",
		ImprovementEntryList.as_view(),
		name="improvement-entry-list-date"
		),
	path(
		'api/users/<str:slug>/emotions/',
		EmotionEntryList.as_view(),
		name='emotion-entry-list-all'
		),
	path(
		"api/users/<str:slug>/emotions/<str:date_request>/<int:pk>/",
		EmotionEntryDetail.as_view(),
		name="emotion-entry-detail-single"
		),
	path(
		"api/users/<str:slug>/emotions/<str:date_request>/",
		EmotionEntryList.as_view(),
		name="emotion-entry-list-date"
		)
	]