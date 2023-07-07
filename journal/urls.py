from django.urls import path

from .api_views.appointment_entries import AppointmentEntryList, \
    AppointmentEntryDetail
from .api_views.target_entries import TargetEntryList, TargetEntryDetail
from .api_views.note_entries import NoteEntryList, NoteEntryDetail
from .api_views.knowledge_entries import KnowledgeEntryList, \
    KnowledgeEntryDetail
from .api_views.gratitude_entries import GratitudeEntryList, \
    GratitudeEntryDetail
from .api_views.win_entries import WinEntryList, WinEntryDetail
from .api_views.ideas_entries import IdeasEntryList, IdeasEntryDetail
from .api_views.improvement_entries import ImprovementEntryList, \
    ImprovementEntryDetail
from .api_views.custom_user import CustomUserList, CustomUserDetail

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
    path(
        "api/gratitude/<str:date_request>/<int:pk>/",
        GratitudeEntryDetail.as_view(),
        name="gratitude-entry-detail"
    ),
    path(
        "api/gratitude/<str:date_request>/",
        GratitudeEntryList.as_view(),
        name="gratitude-entry-list"
    ),
    path(
        "api/wins/<str:date_request>/<int:pk>/",
        WinEntryDetail.as_view(),
        name="win-entry-detail"
    ),
    path(
        "api/wins/<str:date_request>/",
        WinEntryList.as_view(),
        name="win-entry-list"
    ),
    path(
        "api/ideas/<str:date_request>/<int:pk>/",
        IdeasEntryDetail.as_view(),
        name="ideas-entry-detail"
    ),
    path(
        "api/ideas/<str:date_request>/",
        IdeasEntryList.as_view(),
        name="ideas-entry-list"
    ),
    path(
        "api/improvement/<str:date_request>/<int:pk>/",
        ImprovementEntryDetail.as_view(),
        name="improvement-entry-detail"
    ),
    path(
        "api/improvement/<str:date_request>/",
        ImprovementEntryList.as_view(),
        name="improvement-entry-list"
    ),
    path(
        "api/users/<int:pk>/",
        CustomUserDetail.as_view(),
        name="user-detail"
    ),
    path(
        "api/users/",
        CustomUserList.as_view(),
        name="user-list"
    ),
]
