from rest_framework import filters, mixins, viewsets
from api.permissions import AdminAddDeletePermission
from rest_framework.pagination import PageNumberPagination


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
