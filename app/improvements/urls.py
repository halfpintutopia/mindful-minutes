from django.urls import path

from .views import (
    ImprovementEntryDetail,
    ImprovementEntryList,
    ImprovementEntryListCreate,
)

urlpatterns = [
    path(
        "api/users/<str:slug>/improvement/",
        ImprovementEntryList.as_view(),
        name="improvement-entry-list",
    ),
    path(
        "api/users/<str:slug>/improvement/<str:date_request>/",
        ImprovementEntryListCreate.as_view(),
        name="improvement-entry-date-list",
    ),
    path(
        "api/users/<str:slug>/improvement/<str:date_request>/<int:pk>/",
        ImprovementEntryDetail.as_view(),
        name="improvement-entry-detail",
    ),
]
