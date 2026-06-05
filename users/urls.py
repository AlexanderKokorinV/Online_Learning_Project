from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from users.apps import UsersConfig
from users.views import PaymentsListAPIView, UserProfileUpdateView, UserCreateAPIView, UserListAPIView, \
    UserDestroyAPIView

app_name = UsersConfig.name


urlpatterns = [
    # Маршруты CRUD пользователей
    path("users/create/", UserCreateAPIView.as_view(), name="user_create"),
    path("users/", UserListAPIView.as_view(), name="user_list"),
    path("users/profile/<int:pk>/", UserProfileUpdateView.as_view(), name="user_profile"),
    path("users/delete/<int:pk>/", UserDestroyAPIView.as_view(), name="user_delete"),

    # Список платежей
    path("payments/", PaymentsListAPIView.as_view(), name="payments_list"),

    #  # Авторизация JWT
    path("token/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
]
