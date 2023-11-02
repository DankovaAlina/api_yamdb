from rest_framework import permissions 
from rest_framework.permissions import BasePermission, SAFE_METHODS 
 
from reviews.models import User 
 
 
def get_user(user_id): 
    """ 
    Получает пользователя по id. 
    """ 
    if user_id: 
        user = User.objects.filter(id=user_id).first() 
        return user 
    return None 
 
 
class IsAdmin(permissions.BasePermission): 
    """ 
    Проверяет, является ли пользователь администратором или суперюзером. 
    """ 
 
    def has_permission(self, request, view): 
        user = get_user(request.user.id) 
        return user and (user.role == 'admin' or user.is_superuser) 
 
    def has_object_permission(self, request, view, obj): 
        user = get_user(request.user.id) 
        return user and (user.role == 'admin' or user.is_superuser) 
 
 
class AdminAddDeletePermission(permissions.IsAdminUser): 
    """ 
    Разрешение администраторам на добавление и удаление. 
    """ 
 
    def has_permission(self, request, view): 
        return ((request.method in SAFE_METHODS) 
                or (request.user.is_authenticated 
                    and request.user.role == 'admin')) 
 
 
class IsAdminAuthorOrReadOnly(BasePermission): 
    """ 
    Проверяет, что вносить изменения могут 
    только администратор или автор объекта. 
    """ 
 
    def has_permission(self, request, view):
        return bool(
            request.method in permissions.SAFE_METHODS
            or request.user.is_authenticated
        )

    def has_object_permission(self, request, view, obj):
        return bool(
            request.method in permissions.SAFE_METHODS
            or obj.author == request.user
            or request.user.role == 'moderator'
            or request.user.role == 'admin'
        )
