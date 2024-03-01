from django.urls import path

from .views import (
    TargetEntryDetail,
    TargetEntryList,
    TargetEntryListCreate,
)

urlpatterns = [
    path(
        "api/users/<str:slug>/target/",
        TargetEntryList.as_view(),
        name="target-entry-list",
    ),
    path(
        "api/users/<str:slug>/target/<str:date_request>/",
        TargetEntryListCreate.as_view(),
        name="target-entry-date-list",
    ),
    path(
        "api/users/<str:slug>/target/<str:date_request>/<int:pk>/",
        TargetEntryDetail.as_view(),
        name="target-entry-detail",
    ),
]
