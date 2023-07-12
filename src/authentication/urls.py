from django.urls import path
from drf_yasg.utils import swagger_auto_schema
from rest_framework_simplejwt.views import (TokenObtainPairView,
                                            token_obtain_pair)

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
