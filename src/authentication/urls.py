from django.urls import path
from drf_yasg.utils import swagger_auto_schema
from rest_framework_simplejwt.views import TokenObtainPairView  # noqa
from rest_framework_simplejwt.views import token_obtain_pair  # noqa

from authentication.serializers import LoginResponseSerializer

urlpatterns = [
    path(
        "token/",
        swagger_auto_schema(method="post", responses={201: LoginResponseSerializer})(
            TokenObtainPairView.as_view()
        ),
    ),
]
