from django.urls import path

from .views import (
    NoteEntryDetail,
    NoteEntryList,
    NoteEntryListCreate,
)

urlpatterns = [
    path(
        "api/users/<str:slug>/note/",
        NoteEntryList.as_view(),
        name="note-entry-list",
    ),
    path(
        "api/users/<str:slug>/note/<str:date_request>/",
        NoteEntryListCreate.as_view(),
        name="note-entry-date-list",
    ),
    path(
        "api/users/<str:slug>/note/<str:date_request>/<int:pk>/",
        NoteEntryDetail.as_view(),
        name="note-entry-detail",
    ),
]
