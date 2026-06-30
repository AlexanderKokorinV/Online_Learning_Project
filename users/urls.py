from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from users.apps import UsersConfig
from users.views import (
    PaymentsListCreateAPIView,
    PaymentStatusAPIView,
    UserCreateAPIView,
    UserDestroyAPIView,
    UserListAPIView,
    UserProfileUpdateView,
)

app_name = UsersConfig.name


urlpatterns = [
    # Маршруты CRUD пользователей
    path("create/", UserCreateAPIView.as_view(), name="user_create"),
    path("", UserListAPIView.as_view(), name="user_list"),
    path("profile/<int:pk>/", UserProfileUpdateView.as_view(), name="user_profile"),
    path("delete/<int:pk>/", UserDestroyAPIView.as_view(), name="user_delete"),
    # Список платежей
    path("payments/", PaymentsListCreateAPIView.as_view(), name="payments_list_create"),
    path("payments/status/<int:pk>/", PaymentStatusAPIView.as_view(), name="payments_status"),
    #  # Авторизация JWT
    path("token/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
]
