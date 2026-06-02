from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import OrderingFilter
from rest_framework.generics import RetrieveUpdateAPIView, ListAPIView

from users.models import User, Payments
from users.serializers import UserProfileSerializer, PaymentsSerializer


# Create your views here.


class UserProfileUpdateView(RetrieveUpdateAPIView):
    """Эндпоинт для редактирования профиля любого пользователя"""

    queryset = User.objects.prefetch_related("payments__paid_course", "payments__paid_lesson")
    serializer_class = UserProfileSerializer


class PaymentsListAPIView(ListAPIView):
    """Эндпоинт для списка платежей"""

    queryset = Payments.objects.select_related("user", "paid_course", "paid_lesson")
    serializer_class = PaymentsSerializer

    filter_backends = (DjangoFilterBackend, OrderingFilter)
    filterset_fields = ["paid_course", "paid_lesson", "payment_type"]
    ordering_fields = ("payment_date",)
