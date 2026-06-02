from django.urls import path

from users.apps import UsersConfig
from users.views import UserProfileUpdateView, PaymentsListAPIView

app_name = UsersConfig.name


urlpatterns = [
    path("profile/<int:pk>/", UserProfileUpdateView.as_view(), name="user_profile"),
    path("payments/", PaymentsListAPIView.as_view(), name="payments_list"),
]
