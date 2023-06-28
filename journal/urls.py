from django.urls import path

from .api_views.appointment_entries import AppointmentEntryList, \
    AppointmentEntryDetail
from .api_views.targets import TargetList, TargetDetail

urlpatterns = [
    path(
        "api/appointments/",
        AppointmentEntryList.as_view()
    ),
    path(
        "api/appointments/id/<int:pk>/",
        AppointmentEntryDetail.as_view()
    ),
    path(
        "api/appointments/date/<str:date_request>/",
        AppointmentEntryList.as_view()
    ),
    path(
        "api/targets/",
        TargetList.as_view()
    ),
    path(
        "api/targets/id/<int:pk>/",
        TargetDetail.as_view()
    ),
    path(
        "api/targets/date/<str:date_request>/",
        TargetList.as_view()
    ),
]
