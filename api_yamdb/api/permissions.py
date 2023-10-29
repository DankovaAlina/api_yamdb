from rest_framework.permissions import SAFE_METHODS, BasePermission

from reviews.models import User


class IsAdminAuthorOrReadOnly(BasePermission):

    """Проверяет, что вносить изменения могут только администратор или автор объекта."""

    def get_user(self, user_id):
        """Получает пользователя по id."""
        if user_id:
            user = User.objects.filter(id=user_id).first()
            return user
        return None

    def has_object_permission(self, request, view, obj):
        user = self.get_user(request.user.id)
        if request.method in SAFE_METHODS:
            return True
        if request.method == 'POST':
            return request.user.is_authenticated
        return (request.user.is_authenticated and (
            request.user == obj.author
            or user.role in ('admin', 'moderator')
        ))
