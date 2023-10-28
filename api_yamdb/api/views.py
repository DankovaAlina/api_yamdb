from django.shortcuts import render
from .serializers import CategorySerializer, GenreSerializer, TitleSerializer
from rest_framework.viewsets import ModelViewSet
from reviews.models import Category, Genre, Title
from .permissions import AdminAddDeletePermission
from django.shortcuts import get_object_or_404


class CategoryViewSet(ModelViewSet):
    """
    Вьюсет категории.
    """

    serializer_class = CategorySerializer
    permission_classes = (AdminAddDeletePermission,)
    http_method_names = ('get', 'post', 'delete')
    lookup_field = 'slug'
    queryset = Category.objects.all()


class GenreViewSet(ModelViewSet):
    """
    Вьюсет жанра.
    """

    serializer_class = GenreSerializer
    permission_classes = (AdminAddDeletePermission,)
    http_method_names = ('get', 'post', 'delete')
    lookup_field = 'slug'
    queryset = Genre.objects.all()


class TitleViewSet(ModelViewSet):
    """
    Вьюсет заголовка.
    """

    serializer_class = TitleSerializer
    permission_classes = (AdminAddDeletePermission,)
    queryset = Title.objects.all()

    def get_serializer_context(self):
        """
        Переопределение метода для добавления context в сериализатор.
        """
        context = super().get_serializer_context()
        context['genres'] = Genre.objects.all()
        return context
