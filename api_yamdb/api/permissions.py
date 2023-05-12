from rest_framework import permissions


class IsAdmin(permissions.BasePermission):
    """Проверка на администратора или суперюзера."""

    def has_permission(self, request, view):
        return (request.user.is_authenticated
                and (request.user.is_admin or request.user.is_superuser))


class IsAuthenticatedOrReadOnly(permissions.BasePermission):
    """
    Разрешает доступ аутентифицированным пользователям,
    остальным только для чтения.
    """

    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        return request.user and request.user.is_authenticated

      
class IsAdminOrReadOnly(permissions.BasePermission):
    """
    Права на изменение только для администраторов, для
    остальных доступ только для чтения.
    """

    def has_permission(self, request, view):
        return (
            request.method in permissions.SAFE_METHODS
            or request.user.is_authenticated
            and (request.user.is_admin or request.user.is_superuser)
        )
