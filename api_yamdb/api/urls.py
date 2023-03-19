from api.views import (CommentViewSet, ReViewSet)
from django.urls import include, path
from rest_framework.routers import DefaultRouter
from .views import CategoryViewSet, GenreViewSet, TitleViewSet
from api.views import (UserViewSet)
from django.urls import include, path
from rest_framework.routers import DefaultRouter
from .views import (get_jwt_token,
                    sign_up)




v1_router = DefaultRouter()
v1_router.register('users', UserViewSet, basename='users')
v1_router.register(r'categories', CategoryViewSet, basename='categories')
v1_router.register(r'genres', GenreViewSet, basename='genres')
v1_router.register(r'titles', TitleViewSet, basename='titles')
v1_router.register(r'titles/(?P<title_id>\d+)/reviews',
                ReViewSet, basename='ReViewSet')
v1_router.register(
    r'titles/(?P<title_id>\d+)/reviews/(?P<review_id>\d+)/comments',
    CommentViewSet, basename='CommentViewSet'
)

urlpatterns = [
    path('v1/', include(v1_router.urls)),
    path('v1/auth/token/', get_jwt_token, name='get_token'),
    path('v1/auth/signup/', sign_up, name='signup'),
]

# jwtpatterns = [
#     path('token/', get_jwt_token, name='token_obtain_pair'),
#     path('signup/', sign_up, name='signup'),
# ]
