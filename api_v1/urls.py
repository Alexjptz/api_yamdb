from django.urls import include, path
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import (TokenObtainPairView,
                                            TokenRefreshView)

from .views import CommentsViewSet, ReviewsViewSet, create_user
from .serializers import GetMyTokenSerializer

v1_router = DefaultRouter()
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

auth_patterns = [
    path('email/', create_user, name='create_user'),
    path('token/', TokenObtainPairView.as_view(
        serializer_class=GetMyTokenSerializer),
        name='token_obtain'
    ),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]

urlpatterns = [
    path('v1/', include(v1_router.urls)),
    path('v1/auth/', include(auth_patterns)),
]
