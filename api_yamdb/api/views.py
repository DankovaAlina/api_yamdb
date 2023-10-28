from django.shortcuts import get_object_or_404
from rest_framework.viewsets import ModelViewSet

from reviews.models import Category, Genre, Title
from .serializers import CategorySerializer, GenreSerializer, TitleSerializer
from .permissions import AdminAddDeletePermission
from .mixins import ListCreateDestroyViewSet


class CategoryViewSet(ListCreateDestroyViewSet):
    """
    Вьюсет категории.
    """

    serializer_class = CategorySerializer
    permission_classes = (AdminAddDeletePermission,)
    queryset = Category.objects.all()


class GenreViewSet(ListCreateDestroyViewSet):
    """
    Вьюсет жанра.
    """

    serializer_class = GenreSerializer
    permission_classes = (AdminAddDeletePermission,)
    queryset = Genre.objects.all()


class TitleViewSet(ModelViewSet):
    """
    Вьюсет заголовка.
    """

    serializer_class = TitleSerializer
    permission_classes = (AdminAddDeletePermission,)
    queryset = Title.objects.all()

    def perform_create(self, serializer):
        category = get_object_or_404(
            Category, slug=self.request.data.get('category')
        )
        genre = Genre.objects.filter(
            slug__in=self.request.data.getlist('genre')
        )
        serializer.save(category=category, genre=genre)

    def perform_update(self, serializer):
        self.perform_create(serializer)
