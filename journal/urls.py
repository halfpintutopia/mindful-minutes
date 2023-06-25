from django.urls import path

from .views.appointment_entries import AppointmentEntryList, AppointmentEntryDetail

urlpatterns = [
    path("api/appointments/", AppointmentEntryList.as_view()),
    path("api/appointments/id/<int:pk>/", AppointmentEntryDetail.as_view()),
    path("api/appointments/date/<str:date_request>/", AppointmentEntryList.as_view()),
]
