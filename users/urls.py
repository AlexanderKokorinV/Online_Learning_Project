from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from users.apps import UsersConfig
from users.views import PaymentsListAPIView, UserProfileUpdateView

app_name = UsersConfig.name


urlpatterns = [
    path("profile/<int:pk>/", UserProfileUpdateView.as_view(), name="user_profile"),
    path("payments/", PaymentsListAPIView.as_view(), name="payments_list"),

    # simple-jwt
    path("token/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
]
