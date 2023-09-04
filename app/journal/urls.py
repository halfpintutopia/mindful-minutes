from django.urls import path

from .views.index_views import index
from .views.index_views import design_system

urlpatterns = [
    path("", index, name="home"),
    path("design-system", design_system, name="design-systems"),
]
