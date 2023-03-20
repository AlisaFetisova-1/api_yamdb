from api.views import (
    CategoryViewSet,
    CommentViewSet,
    GenreViewSet,
    ReViewSet,
    TitleViewSet,
    UserViewSet,
    get_jwt_token,
    sign_up
)
from django.urls import include, path
from rest_framework.routers import DefaultRouter

v1_router = DefaultRouter()
v1_router.register(r'users', UserViewSet, basename='users')
v1_router.register(r'categories', CategoryViewSet, basename='categories')
v1_router.register(r'genres', GenreViewSet, basename='genres')
v1_router.register(r'titles', TitleViewSet, basename='titles')
v1_router.register(
    r'titles/(?P<title_id>\d+)/reviews',
    ReViewSet, basename='reviews')
v1_router.register(
    r'titles/(?P<title_id>\d+)/reviews/(?P<review_id>\d+)/comments',
    CommentViewSet, basename='comments'
)

urlpatterns = [
    path('v1/', include(v1_router.urls)),
    path('v1/auth/token/', get_jwt_token, name='get_token'),
    path('v1/auth/signup/', sign_up, name='signup'),
]
