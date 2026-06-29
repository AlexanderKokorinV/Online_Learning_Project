from rest_framework.permissions import BasePermission


class IsModerator(BasePermission):
    """Класс прав доступа для модераторов.
    Разрешает только чтение (GET) и редактирование (PUT/PATCH).
    Запрещает создание (POST) и удаление (DELETE)."""

    def has_permission(self, request, view):
        """Проверка принадлежности к модераторам"""
        return (
            request.user and request.user.is_authenticated and request.user.groups.filter(name="moderators").exists()
        )
