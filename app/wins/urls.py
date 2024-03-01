from django.urls import path

from .views import (
    WinEntryDetail,
    WinEntryList,
    WinEntryListCreate,
)

urlpatterns = [
    path(
        "api/users/<str:slug>/win/",
        WinEntryList.as_view(),
        name="win-entry-list",
    ),
    path(
        "api/users/<str:slug>/win/<str:date_request>/",
        WinEntryListCreate.as_view(),
        name="win-entry-date-list",
    ),
    path(
        "api/users/<str:slug>/win/<str:date_request>/<int:pk>/",
        WinEntryDetail.as_view(),
        name="win-entry-detail",
    ),
]
