from django.contrib import admin
from django.urls import include, path

from users.api import UserCreateAPIView

urlpatterns = [
    path("admin/", admin.site.urls),
    path("auth/", include("authentication.urls")),
    path("users/", include("users.urls")),
    path("tickets/", include("tickets.urls")),
]
