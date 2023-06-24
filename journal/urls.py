from django.urls import path

from .views import AppointmentEntryList

urlpatterns = [
    path("api/appointments/", AppointmentEntryList.as_view())
]