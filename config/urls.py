from django.urls import path
from django.contrib import admin

from core.api import create_user


urlpatterns = [
    path("admin/", admin.site.urls),
    path("users/", create_user),
]