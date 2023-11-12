from rest_framework import filters, generics, mixins, viewsets
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response

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
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)
