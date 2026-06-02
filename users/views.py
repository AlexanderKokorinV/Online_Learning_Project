from rest_framework.generics import RetrieveUpdateAPIView, ListAPIView

from users.models import User, Payments
from users.serializers import UserProfileSerializer, PaymentsSerializer


# Create your views here.


class UserProfileUpdateView(RetrieveUpdateAPIView):
    """Эндпоинт для редактирования профиля любого пользователя"""

    queryset = User.objects.all()
    serializer_class = UserProfileSerializer


class PaymentsListAPIView(ListAPIView):
    """Эндпоинт для списка платежей"""

    queryset = Payments.objects.select_related("user", "paid_course", "paid_lesson")
    serializer_class = PaymentsSerializer
