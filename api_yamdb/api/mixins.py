from rest_framework import filters, generics, mixins, status, viewsets
from rest_framework.pagination import PageNumberPagination

from api.permissions import AdminAddDeletePermission


class MixinCategoryGenre(
    mixins.ListModelMixin,
    mixins.CreateModelMixin,
    mixins.DestroyModelMixin,
    viewsets.GenericViewSet
):
    lookup_field = 'slug'
    filter_backends = [filters.SearchFilter]
    search_fields = ['name']
    permission_classes = (AdminAddDeletePermission,)
    pagination_class = PageNumberPagination


class UserAuthMixin(generics.CreateAPIView):
    """Миксин для пользователей."""

    def post(self, request, *args, **kwargs):
        response = super().post(request, *args, **kwargs)
        response.status_code = status.HTTP_200_OK
        return response
