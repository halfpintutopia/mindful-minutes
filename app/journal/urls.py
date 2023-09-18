from django.urls import path

from .views.index_views import design_system, index

urlpatterns = [
    path("", index, name="home"),
    path("design-system", design_system, name="design-systems"),
]
