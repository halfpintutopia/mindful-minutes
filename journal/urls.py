from django.urls import path

from .api_views.appointment_entries import AppointmentEntryList, \
    AppointmentEntryDetail
from .api_views.target_entries import TargetEntryList, TargetEntryDetail
from .api_views.note_entries import NoteEntryList, NoteEntryDetail
from .api_views.knowledge_entries import KnowledgeEntryList, \
    KnowledgeEntryDetail

urlpatterns = [
    path(
        "api/appointments/<str:date_request>/<int:pk>/",
        AppointmentEntryDetail.as_view(),
        name="appointment-entry-detail"
    ),
    path(
        "api/appointments/<str:date_request>/",
        AppointmentEntryList.as_view(),
        name="appointment-entry-list"
    ),
    path(
        "api/targets/<str:date_request>/<int:pk>/",
        TargetEntryDetail.as_view(),
        name="target-entry-detail"
    ),
    path(
        "api/targets/<str:date_request>/",
        TargetEntryList.as_view(),
        name="target-entry-list"
    ),
    path(
        "api/notes/<str:date_request>/<int:pk>/",
        NoteEntryDetail.as_view(),
        name="note-entry-detail"
    ),
    path(
        "api/notes/<str:date_request>/",
        NoteEntryList.as_view(),
        name="note-entry-list"
    ),
    path(
        "api/knowledge/<str:date_request>/<int:pk>/",
        KnowledgeEntryDetail.as_view(),
        name="knowledge-entry-detail"
    ),
    path(
        "api/knowledge/<str:date_request>/",
        KnowledgeEntryList.as_view(),
        name="knowledge-entry-list"
    ),
]
