from rest_framework.permissions import (
    BasePermission, IsAdminUser, SAFE_METHODS
)

from reviews.models import User


class IsAdmin(BasePermission):
    """
    Проверяет, является ли пользователь администратором или суперюзером.
    """

    def has_permission(self, request, view):
        user = User.objects.filter(id=request.user.id).first()
        return user and user.is_admin

    def has_object_permission(self, request, view, obj):
        user = User.objects.filter(id=request.user.id).first()
        return user and user.is_admin


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
    только администратор или автор объекта.
    """

    def has_object_permission(self, request, view, obj):
        user = User.objects.filter(id=request.user.id).first()
        if request.method in SAFE_METHODS:
            return True
        if request.method == 'POST':
            return request.user.is_authenticated
        return (request.user.is_authenticated and (
            request.user == obj.author or user.is_moderator
        ))
