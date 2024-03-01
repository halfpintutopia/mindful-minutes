"""
URL configuration for mindfulminutes project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import include, path
from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from rest_framework import permissions
from .views import (
    account_page,
    design_system,
    evening_page,
    index,
    morning_page,
    search,
)

schema_view = get_schema_view(
    openapi.Info(
        title="Mindful Minutes API",
        default_version="v1",
    ),
    public=True,
    permission_classes=[permissions.AllowAny],
)

urlpatterns = [
    path("admin/", admin.site.urls),
    path("accounts/", include("allauth.urls")),
    path("accounts/", include("allauth.socialaccount.urls")),
    path("", include("appointments.urls")),
    path("", include("emotions.urls")),
    path("", include("gratitude_entries.urls")),
    path("", include("ideas.urls")),
    path("", include("improvements.urls")),
    path("", include("knowledge_entries.urls")),
    path("", include("notes.urls")),
    path("", include("targets.urls")),
    path("", include("users.urls")),
    path("", include("wins.urls")),
    path("", index, name="home"),
    path("search/", search, name="search"),
    path("account/", account_page, name="account"),
    path("morning/", morning_page, name="morning"),
    path("evening/", evening_page, name="evening"),
    path("design-system", design_system, name="design-systems"),
    path(
        "swagger-docs/",
        schema_view.with_ui("swagger", cache_timeout=0),
        name="schema-swagger-ui",
    ),
]
