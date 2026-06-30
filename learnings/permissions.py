from rest_framework.permissions import BasePermission


class IsModerator(BasePermission):
    """Проверяет, является ли пользователь модератором"""
    def has_permission(self, request, view):
        if not request.user or not request.user.is_authenticated:
            return False
        return request.user.is_staff or request.user.groups.filter(name="moderators").exists()


class IsOwner(BasePermission):
    """Проверяет, является ли пользователь владельцем конкретного объекта"""
    def has_object_permission(self, request, view, obj):
        if not hasattr(obj, 'user') or obj.user is None:
            return False
        return obj.user == request.user


class IsNotModerator(BasePermission):
    """Разрешает доступ всем, кроме модераторов"""
    def has_permission(self, request, view):
        if not request.user or not request.user.is_authenticated:
            return False
        is_mod = request.user.is_staff or request.user.groups.filter(name="moderators").exists()
        return not is_mod


class IsOwnerOrModerator(BasePermission):
    """Разрешает доступ либо владельцу объекта, либо модератору"""
    def has_permission(self, request, view):
        # На уровне списка (список фильтруется в get_queryset) разрешаем авторизованным
        return request.user and request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        # На уровне конкретного объекта: проверяем, модератор или владелец
        is_mod = request.user.is_staff or request.user.groups.filter(name="moderators").exists()
        is_owner = hasattr(obj, 'user') and obj.user == request.user
        return is_owner or is_mod
