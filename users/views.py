from rest_framework.generics import RetrieveUpdateAPIView

from users.models import User
from users.serializers import UserProfileSerializer


# Create your views here.


class UserProfileUpdateView(RetrieveUpdateAPIView):
    """Эндпоинт для редактирования профиля любого пользователя"""
    queryset = User.objects.all()
    serializer_class = UserProfileSerializer