from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import status
from rest_framework.filters import OrderingFilter
from rest_framework.generics import (
    CreateAPIView,
    DestroyAPIView,
    ListAPIView,
    ListCreateAPIView,
    RetrieveUpdateAPIView,
)
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from learnings.permissions import IsModerator
from users.models import Payments, User
from users.permissions import IsOwner
from users.serializers import (
    PaymentsCreateSerializer,
    PaymentsSerializer,
    UserProfileSerializer,
    UserPublicProfileSerializer,
    UserRegisterSerializer,
)
from users.services import create_stripe_price, create_stripe_product, create_stripe_session, retrieve_stripe_session

# Create your views here.

# -----CRUD пользователей-----


class UserCreateAPIView(CreateAPIView):
    """Эндпоинт для регистрации пользователей (доступен всем)"""

    serializer_class = UserRegisterSerializer
    queryset = User.objects.all()
    permission_classes = [AllowAny]  # Открываем эндпоинт для неавторизованных пользователей


class UserListAPIView(ListAPIView):
    """Эндпоинт для списка пользователей (доступен только авторизованным)"""

    queryset = User.objects.prefetch_related("payments__paid_course", "payments__paid_lesson")

    def get_serializer_class(self):
        """Модераторы и персонал видят полный список со всеми платежами.
        Остальные пользователи - только общую инфо"""
        user = self.request.user
        if user.is_authenticated and (
            user.is_staff or user.is_superuser or user.groups.filter(name="moderators").exists()
        ):
            return UserProfileSerializer  # Полный профиль

        return UserPublicProfileSerializer  # Только общая инфо


class UserProfileUpdateView(RetrieveUpdateAPIView):
    """Эндпоинт для просмотра и редактирования профиля любого пользователя"""

    queryset = User.objects.prefetch_related("payments__paid_course", "payments__paid_lesson")

    def get_permissions(self):
        """Просмотр (GET) - все авторизованные, PUT/PATCH - только владелец или модератор"""
        if self.request.method == "GET":
            return [IsAuthenticated()]

        user = self.request.user
        if user.is_authenticated and user.groups.filter(name="moderators").exists():
            return [IsAuthenticated()]

        return [IsAuthenticated(), IsOwner()]

        return [IsAuthenticated(), IsModerator() | IsOwner()]

    def get_serializer_class(self):
        """Если владелец - доступ ко всем данным, остальным - только общая инфо"""

        # Получаем объект пользователя
        obj = self.get_object()
        current_user = self.request.user

        if (
            current_user == obj
            or current_user.is_staff
            or current_user.is_superuser
            or current_user.groups.filter(name="moderators").exists()
        ):
            return UserProfileSerializer  # Полный профиль

        return UserPublicProfileSerializer  # Только общая инфо


class UserDestroyAPIView(DestroyAPIView):
    """Эндпоинт для удаления пользователей (только для админов и владельцев)"""

    queryset = User.objects.all()
    serializer_class = UserProfileSerializer

    def get_permissions(self):

        user = self.request.user

        if user.is_authenticated and (user.is_staff or user.is_superuser):
            return [IsAuthenticated()]

        return [IsAuthenticated(), IsOwner()]


# -----Платежи-----


class PaymentsListCreateAPIView(ListCreateAPIView):
    """Эндпоинт для следующих запросов:
    GET - Просмотр списка платежей текущего пользователя с фильтрацией.
    POST - Инициализация покупки курса и генерация платежной ссылки Stripe.
    """

    queryset = Payments.objects.select_related("user", "paid_course", "paid_lesson")

    filter_backends = (DjangoFilterBackend, OrderingFilter)

    filterset_fields = ["paid_course", "paid_lesson", "payment_type"]
    ordering_fields = ("created_at",)

    permission_classes = [IsAuthenticated]

    def get_serializer_class(self):
        """Выбор сериализатора (для чтения или создания)"""
        if self.request.method == "POST":
            return PaymentsCreateSerializer
        return PaymentsSerializer

    def perform_create(self, serializer):
        """Метод для создания платежа и интеграции со Stripe при POST-запросе"""
        course = serializer.validated_data.get("paid_course")

        amount = getattr(course, "price", 5000)

        # Запросы к Stripe через сервисный модуль (services.py)
        product_data = create_stripe_product(course.title)
        price_data = create_stripe_price(product_data["id"], amount)
        session_data = create_stripe_session(price_data["id"])

        # Сохранение всех данных в модель Payments
        serializer.save(
            user=self.request.user,
            payment_amount=amount,
            payment_type="stripe",
            payment_link=session_data["url"],
            session_id=session_data["id"],
            status=session_data["status"],
        )


class PaymentStatusAPIView(APIView):
    """Контроллер для проверки актуального статуса платежа в Stripe по его ID"""

    permission_classes = [IsAuthenticated]

    def get(self, request, pk):
        # Платеж текущего пользователя по ID
        payment = get_object_or_404(Payments, pk=pk, user=request.user)

        if not payment.session_id:
            return Response({"error": "Этот платеж не связан со Stripe"}, status=status.HTTP_400_BAD_REQUEST)

        # Запрашиваем актуальный статус у Stripe API (services.py)
        stripe_data = retrieve_stripe_session(payment.session_id)

        # Обновляем статус в БД
        payment.status = stripe_data["status"]
        payment.save()

        return Response(
            {
                "payment_id": payment.id,
                "course": payment.paid_course.title if payment.paid_course else "Урок",
                "amount": payment.payment_amount,
                "stripe_status": stripe_data["status"],  # "open", "complete", "expired"
                "payment_status": stripe_data["payment_status"],  # "paid" или "unpaid"
            },
            status=status.HTTP_200_OK,
        )
