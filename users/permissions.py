from rest_framework.permissions import BasePermission


class IsOwner(BasePermission):
    """Класс прав доступа для владельцев (создателей курса или урока)"""

    def has_object_permission(self, request, view, obj):
        """Проверка, является ли владельцем"""
        return request.user and request.user.is_authenticated and obj.user == request.user