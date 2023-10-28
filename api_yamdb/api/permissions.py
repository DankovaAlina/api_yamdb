from rest_framework.permissions import IsAdminUser


class AdminAddDeletePermission(IsAdminUser):
    """
    Разрешение администраторам на добавление и удаление.
    """

    def has_permission(self, request, view):
        return bool((request.method == 'GET')
                    or (request.user and request.user.is_staff))
