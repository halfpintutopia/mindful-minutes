from django.urls import path

from .views import EmotionEntryDetail, EmotionEntryList, EmotionEntryListCreate

urlpatterns = [
    path(
        "api/users/<str:slug>/emotions/",
        EmotionEntryList.as_view(),
        name="emotion-entry-list",
    ),
    path(
        "api/users/<str:slug>/emotions/<str:date_request>/",
        EmotionEntryListCreate.as_view(),
        name="emotion-entry-date-list",
    ),
    path(
        "api/users/<str:slug>/emotions/<str:date_request>/<int:pk>/",
        EmotionEntryDetail.as_view(),
        name="emotion-entry-detail",
    ),
]
