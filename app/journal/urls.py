from django.urls import path

from .views.index_views import (
    account_page,
    design_system,
    evening_page,
    index,
    morning_page,
    search,
)

urlpatterns = [
    path("", index, name="home"),
    path("search/", search, name="search"),
    path("account/", account_page, name="account"),
    path("morning/", morning_page, name="morning"),
    path("evening/", evening_page, name="evening"),
    path("design-system", design_system, name="design-systems"),
]
