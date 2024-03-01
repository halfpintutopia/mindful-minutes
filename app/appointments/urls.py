from django.urls import path

from .views import (
    AppointmentEntryDetail,
    AppointmentEntryList,
    AppointmentEntryListCreate,
)

urlpatterns = [
    path(
        "api/users/<str:slug>/appointments/",
        AppointmentEntryList.as_view(),
        name="appointment-entry-list",
    ),
    path(
        "api/users/<str:slug>/appointments/<str:date_request>/",
        AppointmentEntryListCreate.as_view(),
        name="appointment-entry-date-list",
    ),
    path(
        "api/users/<str:slug>/appointments/<str:date_request>/<int:pk>/",
        AppointmentEntryDetail.as_view(),
        name="appointment-entry-detail",
    ),
]
