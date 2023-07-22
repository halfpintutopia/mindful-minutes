from django.urls import path

from .views.index_views import index

urlpatterns = [
    path("", index, name="home"),
]
