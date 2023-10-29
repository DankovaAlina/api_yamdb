from django.urls import include, path
from rest_framework import routers


from api.views import UserSignup, UserToken, UserViewSet, GenreViewSet, CategoryViewSet, TitleViewSet

app_name = 'api'
  
router_v1 = routers.DefaultRouter()
router_v1.register('users', UserViewSet, basename='users')
router_v1.register('titles', TitleViewSet, basename='titles')
router_v1.register('categories', CategoryViewSet, basename='categories')
router_v1.register('genres', GenreViewSet, basename='genres')


urlpatterns = [
    path('v1/', include(router_v1.urls)),
    path('v1/auth/signup/', UserSignup.as_view()),
    path('v1/auth/token/', UserToken.as_view()),
    path('v1/', include(router_v1.urls)),
]
