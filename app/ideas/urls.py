from django.urls import path

from .views import IdeasEntryDetail, IdeasEntryList, IdeasEntryListCreate

urlpatterns = [
    path(
        "api/users/<str:slug>/ideas/",
        IdeasEntryList.as_view(),
        name="ideas-entry-list",
    ),
    path(
        "api/users/<str:slug>/ideas/<str:date_request>/",
        IdeasEntryListCreate.as_view(),
        name="ideas-entry-date-list",
    ),
    path(
        "api/users/<str:slug>/ideas/<str:date_request>/<int:pk>/",
        IdeasEntryDetail.as_view(),
        name="ideas-entry-detail",
    ),
]
