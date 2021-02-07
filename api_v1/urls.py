from django.urls import include, path
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import (TokenObtainPairView,
                                            TokenRefreshView)

from .serializers import GetMyTokenSerializer
from .views import (CategoryViewSet, CommentsViewSet, CreateUser, GenreViewSet,
                    ReviewsViewSet, TitleViewSet,
                    UserPersonalData, UsersListCreateViewSet)

v1_router = DefaultRouter()
v1_router.register('users', UsersListCreateViewSet, basename='user-list')
v1_router.register(
    'titles/(?P<title_id>[0-9]+)/reviews',
    ReviewsViewSet,
    basename='review-list'
)
v1_router.register(
    'titles/(?P<title_id>[0-9]+)/reviews/(?P<review_id>[0-9]+)/comments',
    CommentsViewSet,
    basename='comment-list'
)
v1_router.register('categories', CategoryViewSet, basename='categories')
v1_router.register('genres', GenreViewSet, basename='genres')
v1_router.register('titles', TitleViewSet, basename='titles')

auth_patterns = [
    path('email/', CreateUser.as_view(), name='create_user'),
    path('token/', TokenObtainPairView.as_view(
        serializer_class=GetMyTokenSerializer),
        name='token_obtain'
    ),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]

urlpatterns = [
    path('v1/users/me/', UserPersonalData.as_view(), name='personal_data'),
    path('v1/', include(v1_router.urls)),
    path('v1/auth/', include(auth_patterns)),
]
