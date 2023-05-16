from rest_framework import permissions


class IsAdmin(permissions.BasePermission):
    """Проверка на администратора или суперюзера."""

    def has_permission(self, request, view):
        return request.user.is_authenticated and (
            request.user.is_admin
        )  # Не надо тут проверять еще и супера, он уже прописать в админе в модели.


class IsAuthenticatedOrReadOnly(
    permissions.BasePermission
):  # Такой есть у ДРФ
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
            and (request.user.is_admin)
        )  # Не надо тут проверять еще и супера, он уже прописать в админе в модели.


class IsAuthorOrReadOnly(permissions.BasePermission):
    """Права на изменение только для администраторов, автора, модератора, для
    остальных доступ только для чтения.
    """

    def has_permission(self, request, view):
        return (
            request.method in permissions.SAFE_METHODS
            or request.user.is_authenticated
        )

    def has_object_permission(self, request, view, obj):
        return (
            request.method in permissions.SAFE_METHODS
            or obj.author == request.user
            or request.user.is_moderator
            or request.user.is_admin
        )
