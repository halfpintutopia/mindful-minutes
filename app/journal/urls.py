from django.urls import path

from .views.index_views import design_system, index, search

urlpatterns = [
    path("", index, name="home"),
    path("search/", search, name="search"),
    path("design-system", design_system, name="design-systems"),
]
