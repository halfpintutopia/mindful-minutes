from django.urls import path

from .views import (
    KnowledgeEntryDetail,
    KnowledgeEntryList,
    KnowledgeEntryListCreate,
)

urlpatterns = [
    path(
        "api/users/<str:slug>/knowledge/",
        KnowledgeEntryList.as_view(),
        name="knowledge-entry-list",
    ),
    path(
        "api/users/<str:slug>/knowledge/<str:date_request>/",
        KnowledgeEntryListCreate.as_view(),
        name="knowledge-entry-date-list",
    ),
    path(
        "api/users/<str:slug>/knowledge/<str:date_request>/<int:pk>/",
        KnowledgeEntryDetail.as_view(),
        name="knowledge-entry-detail",
    ),
]
