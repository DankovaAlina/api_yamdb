from rest_framework import permissions
from rest_framework.permissions import SAFE_METHODS, BasePermission

from reviews.models import User


class IsAdmin(permissions.BasePermission):
    """Проверяет, является ли пользователь администратором или суперюзером."""

    def get_user(self, user_id):
        """Получает пользователя по id."""
        if user_id:
            user = User.objects.filter(id=user_id).first()
            return user
        return None

    def has_permission(self, request, view):
        user = self.get_user(request.user.id)
        return user and (user.role == 'admin' or user.is_superuser)

    def has_object_permission(self, request, view, obj):
        user = self.get_user(request.user.id)
        return user and (user.role == 'admin' or user.is_superuser)


class IsAdminModeratorAuthorOrReadOnly(BasePermission):

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
 