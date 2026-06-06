from rest_framework.permissions import BasePermission


class IsModerator(BasePermission):
    """Класс прав доступа для модераторов.
    Разрешает только чтение (GET) и редактирование (PUT/PATCH).
    Запрещает создание (POST) и удаление (DELETE)."""
    def has_permission(self, request, view):

        # Проверка существования и авторизации пользователя
        if not request.user or not request.user.is_authenticated:
            return False

        # Проверка принадлежности к группе
        is_moderator = request.user.groups.filter(name="moderators").exists()

        if is_moderator:
            if request.method in ["POST", "DELETE"]:
                return False
            return True

        return False