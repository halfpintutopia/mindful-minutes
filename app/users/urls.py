from django.urls import path

from .views import CustomUserDetail, CustomUserList

urlpatterns = [
    path(
        "api/users/<str:slug>/", CustomUserDetail.as_view(), name="user-detail"
    ),
    path("api/users/", CustomUserList.as_view(), name="user-list"),
]
