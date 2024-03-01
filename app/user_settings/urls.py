from django.urls import path

from .views import UserSettingsView

urlpatterns = [
    path(
        "api/users/<str:slug>/user-settings/",
        UserSettingsView.as_view(),
        name="user-settings",
    ),
]
