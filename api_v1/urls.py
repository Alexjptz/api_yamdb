from django.urls import include, path
from rest_framework import views
from rest_framework.routers import DefaultRouter
from .views import CommentsViewSet, ReviewsViewSet, create_user
from . import views

v1_router = DefaultRouter()
v1_router.register(
    'titles/(?P<title_id>.+)/reviews',
    ReviewsViewSet,
    basename='review-list'
)
v1_router.register(
    'titles/(?P<title_id>.+)/reviews/(?P<review_id>.+)/comments',
    CommentsViewSet,
    basename='comment-list'
)

urlpatterns = [
    path('v1/', include(v1_router.urls)),
    path('v1/auth/email/', views.create_user, name='create_user'),
]