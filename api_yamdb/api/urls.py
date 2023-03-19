from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import get_jwt_token, sign_up
from api.views import UserViewSet

v1_router = DefaultRouter()

v1_router.register('users', UserViewSet, basename='users')

urlpatterns = [
    path('v1/auth/token/', get_jwt_token, name='get_token'),
    path('v1/', include(v1_router.urls)),
    path('v1/auth/signup/', sign_up, name='signup'),
]
