from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import OrderingFilter
from rest_framework.generics import ListAPIView, RetrieveUpdateAPIView, CreateAPIView, DestroyAPIView
from rest_framework.permissions import AllowAny, IsAuthenticated, IsAdminUser

from users.models import Payments, User
from users.permissions import IsOwnerOrStaff
from users.serializers import PaymentsSerializer, UserProfileSerializer, UserRegisterSerializer


# Create your views here.

# -----CRUD пользователей-----

class UserCreateAPIView(CreateAPIView):
    """Эндпоинт для регистрации пользователей (доступен всем)"""
    serializer_class = UserRegisterSerializer
    queryset = User.objects.all()
    permission_classes = [AllowAny] # Открываем эндпоинт для неавторизованных пользователей

class UserListAPIView(ListAPIView):
    """Эндпоинт для списка пользователей (доступен только авторизованным)"""
    serializer_class = UserRegisterSerializer
    queryset = User.objects.prefetch_related("payments__paid_course", "payments__paid_lesson")
    permission_classes = [IsAuthenticated]

class UserProfileUpdateView(RetrieveUpdateAPIView):
    """Эндпоинт для просмотра и редактирования профиля любого пользователя"""
    queryset = User.objects.prefetch_related("payments__paid_course", "payments__paid_lesson")
    serializer_class = UserProfileSerializer
    permission_classes = [IsAuthenticated, IsOwnerOrStaff] # Только владелец или модератор


class UserDestroyAPIView(DestroyAPIView):
    """Эндпоинт для удаления пользователей (только для админов)"""
    queryset = User.objects.all()
    serializer_class = UserProfileSerializer
    permission_classes = [IsAdminUser] #Только админ

# -----Платежи-----

class PaymentsListAPIView(ListAPIView):
    """Эндпоинт для списка платежей (только для авторизованных)"""

    queryset = Payments.objects.select_related("user", "paid_course", "paid_lesson")
    serializer_class = PaymentsSerializer

    filter_backends = (DjangoFilterBackend, OrderingFilter)

    filterset_fields = ["paid_course", "paid_lesson", "payment_type"]
    ordering_fields = ("payment_date",)
    permission_classes = [IsAuthenticated]

