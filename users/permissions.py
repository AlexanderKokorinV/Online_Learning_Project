from rest_framework.permissions import BasePermission


class IsOwnerOrStaff(BasePermission):
    """Катомный класс прав доступа. Проверяет, является ли текущий user владельцем или модератором"""
    def has_object_permission(self, request, view, obj):

        if request.user.is_staff:
            return True

        return request.user == obj.owner