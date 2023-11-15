from rest_framework.permissions import (
    BasePermission, IsAdminUser, SAFE_METHODS
)


class IsAdmin(BasePermission):
    """
    Проверяет, является ли пользователь администратором или суперюзером.
    """

    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.is_admin

    def has_object_permission(self, request, view, obj):
        return request.user.is_authenticated and request.user.is_admin


class AdminAddDeletePermission(IsAdminUser):
    """
    Разрешение администраторам на добавление и удаление.
    """

    def has_permission(self, request, view):
        return ((request.method in SAFE_METHODS)
                or (request.user.is_authenticated
                    and request.user.is_admin))


class IsAdminAuthorOrReadOnly(BasePermission):
    """
    Проверяет, что вносить изменения могут
    только администратор, модератор или автор объекта.
    """

    def has_object_permission(self, request, view, obj):
        if request.method in SAFE_METHODS:
            return True
        if request.method == 'POST':
            return request.user.is_authenticated
        return (request.user.is_authenticated and (
            request.user == obj.author
            or request.user.is_moderator
            or request.user.is_admin
        ))
