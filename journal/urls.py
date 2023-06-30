from django.urls import path

from .api_views.appointment_entries import AppointmentEntryList, \
    AppointmentEntryDetail
from .api_views.target_entries import TargetEntryList, TargetEntryDetail

urlpatterns = [
    path(
        "api/appointments/<str:date_request>/<int:pk>/",
        AppointmentEntryDetail.as_view()
    ),
    path(
        "api/appointments/<str:date_request>/",
        AppointmentEntryList.as_view()
    ),
    path(
        "api/appointments/<str:date_request>/<int:pk>/",
        TargetEntryDetail.as_view()
    ),
    path(
        "api/appointments/<str:date_request>/",
        TargetEntryList.as_view()
    ),
]
