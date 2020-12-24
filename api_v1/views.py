from django.shortcuts import get_object_or_404

from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.pagination import PageNumberPagination
from re import split
from .models import Comments, Reviews, Titles
from .permissions import IsOwnerOrAdminOrReadOnly
from .serializers import CommentsSerializer, CreateUserSerializer, ReviewsSerializer
from users.models import User

from django.core.mail import send_mail
from rest_framework.views import Response, status
from rest_framework.decorators import api_view


@api_view(['POST'])
def create_user(request):
    serialized = CreateUserSerializer(data=request.data)
    if serialized.is_valid():
        username = split(r'@', serialized.data['email'])[0]
        User.objects.create(
            email=serialized.data['email'],
            username=username
        )
        user = User.objects.get(email=serialized.data['email'])
        confirmation_code = User.objects.make_random_password()
        user.set_password(confirmation_code)
        user.save()
        send_mail(
            'Твой код подтверждения',
            'Код подтверждения - {}'.format(confirmation_code),
            'Test@testtest.com',
            ['confirmation_code@test.com']
        )
        return Response(serialized.data, status=status.HTTP_201_CREATED)
    return Response(serialized.errors, status=status.HTTP_400_BAD_REQUEST)


class ReviewsViewSet(viewsets.ModelViewSet):
    serializer_class = ReviewsSerializer
    permission_classes = (IsAuthenticatedOrReadOnly, IsOwnerOrAdminOrReadOnly)

    def get_queryset(self):
        title_id = self.kwargs['title_id']
        title = get_object_or_404(Titles, id=title_id)
        queryset = Reviews.objects.filter(title=title)
        return queryset

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


class CommentsViewSet(viewsets.ModelViewSet):
    serializer_class = CommentsSerializer
    permission_classes = (IsAuthenticatedOrReadOnly, IsOwnerOrAdminOrReadOnly)
    pagination_class = PageNumberPagination

    def get_queryset(self):
        title_id = self.kwargs['title_id']
        title = get_object_or_404(Titles, id=title_id)
        review_id = self.kwargs['review_id']
        review = get_object_or_404(Reviews, title=title, id=review_id)
        queryset = Comments.objects.filter(review=review)
        return queryset

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)