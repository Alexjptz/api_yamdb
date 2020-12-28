from re import split

from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
from rest_framework import filters, permissions, viewsets
from rest_framework.decorators import api_view, permission_classes
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import AllowAny, IsAuthenticatedOrReadOnly
from rest_framework.views import Response, status

from .models import Categories, Comments, Genres, Reviews, Titles
from .permissions import IsModerator, IsOwnerOrAdminOrReadOnly
from .serializers import (CategorySerializer, CommentsSerializer,
                          CreateUserSerializer, GenreSerializer,
                          ReviewsSerializer, TitleSerializerRead,
                          TitleSerializerWrite)

User = get_user_model()


@api_view(['POST'])
@permission_classes([AllowAny])
def create_user(request):
    serialized = CreateUserSerializer(data=request.data)
    if serialized.is_valid():
        confirmation_code = User.objects.make_random_password()
        username = split(r'@', serialized.data['email'])[0]
        user = User.objects.create_user(
            email=serialized.data['email'],
            username=username,
            password=confirmation_code
        )
        user.email_user(
            subject='Код подтверждения',
            message='Твой код подтверждения - {}'.format(confirmation_code),
            from_email='Test@test.com'
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
        title = get_object_or_404(Titles, pk=self.kwargs.get('title_id'))
        is_unqiue = Reviews.objects.filter(
            author=self.request.user,
            title=title
        ).exists()
        if is_unqiue:
            raise ValidationError('You can write only one review.')
        serializer.save(author=self.request.user)


class CommentsViewSet(viewsets.ModelViewSet):
    serializer_class = CommentsSerializer
    permission_classes = [IsOwnerOrAdminOrReadOnly]
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


class CategoryViewSet(viewsets.ModelViewSet):
    permission_classes = [IsOwnerOrAdminOrReadOnly]
    serializer_class = CategorySerializer
    queryset = Categories.objects.all()
    http_method_names = ['get', 'post', 'delete']
    lookup_field = 'slug'
    filter_backends = [filters.SearchFilter]
    search_fields = ['=name']


class GenreViewSet(viewsets.ModelViewSet):
    permission_classes = [IsOwnerOrAdminOrReadOnly]
    serializer_class = GenreSerializer
    queryset = Genres.objects.all()
    http_method_names = ['get', 'post', 'delete']
    lookup_field = 'slug'
    filter_backends = [filters.SearchFilter]
    search_fields = ['=name']


class TitleViewSet(viewsets.ModelViewSet):
    queryset = Titles.objects.all()
    permission_classes = [IsOwnerOrAdminOrReadOnly]
    filter_backends = (filters.SearchFilter)
    search_fields = ['=name', '=year', '=category__slug', '=genre__slug']

    def get_serializer_class(self):
        if self.request.method in permissions.SAFE_METHODS:
            return TitleSerializerRead
        return TitleSerializerWrite
