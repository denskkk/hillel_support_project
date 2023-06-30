from rest_framework.generics import CreateAPIView

from core.serializers import UserCreateRequestSerializer  # noqa
from core.serializers import UserRegistrationSerializer


class UserRegistrationAPIView(CreateAPIView):
    serializer_class = UserRegistrationSerializer

    def post(self, request):
        return super().post(request)
