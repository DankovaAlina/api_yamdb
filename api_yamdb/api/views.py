from django.db.models import Avg
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, viewsets
from rest_framework.decorators import action
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import (
    IsAuthenticated, IsAuthenticatedOrReadOnly)
from rest_framework.response import Response

from api.filters import TitleFilter
from api.mixins import MixinCategoryGenre, UserAuthMixin
from api.permissions import (
    AdminAddDeletePermission, IsAdmin, IsAdminAuthorOrReadOnly
)
from api.serializers import (
    CategorySerializer, CommentSerializer, GenreSerializer,
    ReviewSerializer, TitleReadonlySerializer, TitleCreateDeleteSerializer,
    UserFullInfoSerializer, UserInfoForUserSerializer,
    UserSignupSerializer, UserTokenSerializer
)
from reviews.models import (
    Category, Genre, Review, Title, User
)


class UserSignup(UserAuthMixin):
    """Вьюсет регистрации пользователя."""

    serializer_class = UserSignupSerializer


class UserToken(UserAuthMixin):
    """Вьюсет получения токена."""

    serializer_class = UserTokenSerializer


class UserViewSet(viewsets.ModelViewSet):
    """Вьюсет пользователя."""

    queryset = User.objects.all()
    serializer_class = UserFullInfoSerializer
    permission_classes = (IsAdmin,)
    lookup_field = 'username'
    pagination_class = PageNumberPagination
    filter_backends = (filters.SearchFilter,)
    search_fields = ('username',)
    http_method_names = ['get', 'post', 'patch', 'delete']

    @action(detail=True)
    def get_self_info(self, request):
        """Получение информации о себе."""
        serializer = UserInfoForUserSerializer(self.request.user)
        return Response(serializer.data)

    @action(detail=True)
    def update_self_info(self, request):
        """Редактирование информации о себе."""
        serializer = UserInfoForUserSerializer(
            self.request.user,
            data=request.data,
            partial=True
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

    def get_permissions(self):
        if self.name == 'self_info':
            self.permission_classes = (IsAuthenticated, )
        return super().get_permissions()


class CategoryViewSet(MixinCategoryGenre):
    """Вьюсет категории."""

    serializer_class = CategorySerializer
    queryset = Category.objects.all()


class GenreViewSet(MixinCategoryGenre):
    """Вьюсет жанра."""

    serializer_class = GenreSerializer
    queryset = Genre.objects.all()


class TitleViewSet(viewsets.ModelViewSet):
    """Вьюсет произведения."""

    permission_classes = (AdminAddDeletePermission,)
    http_method_names = ('get', 'post', 'patch', 'delete',)
    queryset = (
        Title.objects.all().annotate(Avg('reviews__score')).order_by('name')
    )
    filter_backends = (DjangoFilterBackend,)
    filterset_class = TitleFilter

    def get_serializer_class(self):
        """Получение произведений."""
        if self.action in ('create', 'update', 'partial_update'):
            return TitleCreateDeleteSerializer
        return TitleReadonlySerializer


class ReviewViewSet(viewsets.ModelViewSet):
    """Вьюсет отзыва."""

    serializer_class = ReviewSerializer
    permission_classes = (IsAuthenticatedOrReadOnly,
                          IsAdminAuthorOrReadOnly)
    http_method_names = ('get', 'post', 'patch', 'delete',)

    def get_title(self):
        """Получение произведения."""
        return get_object_or_404(
            Title,
            id=self.kwargs.get('title_id')
        )

    def get_queryset(self):
        return self.get_title().reviews.all()

    def perform_create(self, serializer):
        serializer.save(
            author=self.request.user,
            title=self.get_title()
        )


class CommentViewSet(viewsets.ModelViewSet):
    """Вьюсет комментария."""

    serializer_class = CommentSerializer
    permission_classes = (IsAuthenticatedOrReadOnly,
                          IsAdminAuthorOrReadOnly)
    http_method_names = ('get', 'post', 'patch', 'delete',)

    def get_review(self):
        """получение отзыва."""
        return get_object_or_404(
            Review,
            id=self.kwargs.get('review_id'),
            title_id=self.kwargs.get('title_id')
        )

    def get_queryset(self):
        return self.get_review().comments.all()

    def perform_create(self, serializer):
        serializer.save(
            author=self.request.user,
            review=self.get_review()
        )
