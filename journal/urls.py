from django.urls import path

from .views import AppointmentEntryList, AppointmentEntryDetail

urlpatterns = [
    path("api/appointments/", AppointmentEntryList.as_view()),
    path("api/appointments/<int:pk>/", AppointmentEntryDetail.as_view()),
]
