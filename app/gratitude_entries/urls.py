from django.urls import path

from .views import (
    GratitudeEntryDetail,
    GratitudeEntryList,
    GratitudeEntryListCreate,
)

urlpatterns = [
    path(
        "api/users/<str:slug>/gratitude/",
        GratitudeEntryList.as_view(),
        name="gratitude-entry-list",
    ),
    path(
        "api/users/<str:slug>/gratitude/<str:date_request>/",
        GratitudeEntryListCreate.as_view(),
        name="gratitude-entry-date-list",
    ),
    path(
        "api/users/<str:slug>/gratitude/<str:date_request>/<int:pk>/",
        GratitudeEntryDetail.as_view(),
        name="gratitude-entry-detail",
    ),
]
