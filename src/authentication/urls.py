from django.urls import path
from rest_framework_simplejwt.views import token_obtain_pair, TokenObtainPairView
from drf_yasg.utils import swagger_auto_schema

from authentication.serializers import LoginResponseSerializer


urlpatterns = [
    path(
        "token/",
        swagger_auto_schema(method="post", responses={201: LoginResponseSerializer})(
            TokenObtainPairView.as_view()
        ),
    ),
    # path("token/refresh/", TokenRefreshView.as_view()),
]