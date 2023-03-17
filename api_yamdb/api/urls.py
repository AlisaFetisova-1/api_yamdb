from api.views import (UserViewSet)
from django.urls import include, path
from rest_framework.routers import DefaultRouter
from .views import (get_jwt_token,
                    sign_up)



router = DefaultRouter()

router.register(
    'users',
    UserViewSet,
    basename='users'
)

# jwtpatterns = [
#     path('token/', get_jwt_token, name='token_obtain_pair'),
#     path('signup/', sign_up, name='signup'),
# ]

urlpatterns = [
    path('v1/auth/token/', get_jwt_token, name='get_token'),
    path('v1/', include(router.urls)),
    path('v1/auth/signup/', sign_up, name='signup'),
]