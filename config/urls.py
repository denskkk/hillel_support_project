from django.contrib import admin
from django.urls import include, path

from core.api import UserRegistrationAPIView

urlpatterns = [
    path("admin/", admin.site.urls),
    path("users/", UserRegistrationAPIView.as_view()),
    path("auth/", include("authentication.urls")),
]
