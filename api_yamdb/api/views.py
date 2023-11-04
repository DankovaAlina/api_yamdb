from django.core.mail import send_mail
from django.db.models import Avg
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, generics, status, viewsets
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import (
    IsAuthenticated, IsAuthenticatedOrReadOnly)
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken

from api.filters import TitleFilter
from api.mixins import MixinCategoryGenre
from api.permissions import (
    AdminAddDeletePermission, IsAdmin, IsAdminAuthorOrReadOnly
)
from api.serializers import (
    CategorySerializer, CommentSerializer, GenreSerializer,
    ReviewSerializer, TitleReadonlySerializer, TitleSerializer,
    UserFullInfoSerializer, UserInfoForUserSerializer,
    UserSignupSerializer, UserTokenSerializer
)
from reviews.models import (
    Category, generate_confirmation_code, Genre, Review, Title, User
)


class UserSignup(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSignupSerializer

    def get_user(self, username, email):
        """Получает пользователя по username и email."""
        return User.objects.filter(
            username=username,
            email=email
        ).first()

    def post(self, request, *args, **kwargs):
        user = self.get_user(
            self.request.data.get('username'),
            self.request.data.get('email')
        )
        if user:
            user.confirmation_code = generate_confirmation_code()
            user.save()
        else:
            serializer = self.get_serializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save()
        user = self.get_user(
            self.request.data.get('username'),
            self.request.data.get('email')
        )
        send_mail(
            subject='Подтверждение регистрации',
            message=f'Код подтверждения - {user.confirmation_code}',
            from_email='api_yamdb@example.com',
            recipient_list=[user.email],
            fail_silently=True,
        )
        return Response(request.data, status=status.HTTP_200_OK)


class UserToken(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserTokenSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = get_object_or_404(
            User,
            username=self.request.data['username']
        )
        if user.confirmation_code != self.request.data['confirmation_code']:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        token = RefreshToken.for_user(user)
        return Response({
            'token': str(token.access_token)
        })


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserInfoForUserSerializer
    permission_classes = [IsAdmin,]
    lookup_field = 'username'
    pagination_class = PageNumberPagination
    filter_backends = (filters.SearchFilter,)
    search_fields = ('username',)
    http_method_names = ['get', 'post', 'patch', 'delete']

    def get_serializer_class(self):
        if self.request.user.role == 'admin' or self.request.user.is_superuser:
            return UserFullInfoSerializer
        return super().get_serializer_class()

    def get_permissions(self):
        if self.kwargs.get('username') == 'me':
            self.permission_classes = [IsAuthenticated,]
        return super().get_permissions()

    def destroy(self, request, *args, **kwargs):
        if self.kwargs.get('username') == 'me':
            return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)
        return super().destroy(request, *args, **kwargs)

    def get_object(self):
        if self.kwargs.get('username') == 'me':
            if self.action in ('retrieve', 'partial_update'):
                return get_object_or_404(User, id=self.request.user.id)
        return super().get_object()


class CategoryViewSet(MixinCategoryGenre):
    """
    Вьюсет категории.
    """

    serializer_class = CategorySerializer
    queryset = Category.objects.all()


class GenreViewSet(MixinCategoryGenre):
    """
    Вьюсет жанра.
    """

    serializer_class = GenreSerializer
    queryset = Genre.objects.all()


class TitleViewSet(viewsets.ModelViewSet):
    """
    Вьюсет произведения.
    """

    permission_classes = (AdminAddDeletePermission,)
    http_method_names = ('get', 'post', 'patch', 'delete',)
    queryset = (
        Title.objects.all().annotate(Avg('reviews__score')).order_by('name')
    )
    filter_backends = (DjangoFilterBackend,)
    filterset_class = TitleFilter

    def get_serializer_class(self):
        """Получение произведений."""
        if self.request.method in ('POST', 'PATCH'):
            return TitleSerializer
        return TitleReadonlySerializer

    def perform_create(self, serializer):
        category = get_object_or_404(
            Category, slug=self.request.data.get('category')
        )
        genre = Genre.objects.filter(
            slug__in=self.request.data.getlist('genre')
        )
        serializer.save(category=category, genre=genre)


class ReviewViewSet(viewsets.ModelViewSet):
    serializer_class = ReviewSerializer
    permission_classes = (IsAuthenticatedOrReadOnly,
                          IsAdminAuthorOrReadOnly)
    http_method_names = ('get', 'post', 'patch', 'delete',)

    def get_title(self):
        return get_object_or_404(
            Title,
            id=self.kwargs.get('title_id')
        )

    def get_queryset(self):
        return self.get_title().reviews.all()

    def perform_create(self, serializer):
        title = self.get_title()
        serializer.save(
            author=self.request.user,
            title=title
        )


class CommentViewSet(viewsets.ModelViewSet):
    serializer_class = CommentSerializer
    permission_classes = (IsAuthenticatedOrReadOnly,
                          IsAdminAuthorOrReadOnly)
    http_method_names = ('get', 'post', 'patch', 'delete',)

    def get_review(self):
        return get_object_or_404(
            Review,
            id=self.kwargs.get('review_id')
        )

    def get_queryset(self):
        return self.get_review().comments.all()

    def perform_create(self, serializer):
        review = self.get_review()
        serializer.save(
            author=self.request.user,
            review=review
        )
