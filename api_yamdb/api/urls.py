from django.urls import path, include
from rest_framework.routers import DefaultRouter

from . import views


app_name = 'api'

router_v1 = DefaultRouter()

router_v1.register('titles', views.TitleViewSet, basename='titles')
router_v1.register('categories', views.CategoryViewSet, basename='categories')
router_v1.register('genres', views.GenreViewSet, basename='genres')

urlpatterns = [
    path('v1/', include(router_v1.urls)),
]
