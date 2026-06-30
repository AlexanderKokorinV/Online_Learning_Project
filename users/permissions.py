from django.contrib.auth import get_user_model
from rest_framework.permissions import BasePermission

User = get_user_model()


class IsOwner(BasePermission):
    """Класс прав доступа для владельцев (создателей курса или урока)"""

    def has_object_permission(self, request, view, obj):
        """Проверка, является ли владельцем"""
        if not request.user or not request.user.is_authenticated:
            return False

        if isinstance(obj, User):
            return obj == request.user

        return getattr(obj, "user", None) == request.user
