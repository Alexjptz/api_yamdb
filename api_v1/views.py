from re import split

from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
from rest_framework import permissions
from rest_framework.exceptions import ValidationError
from rest_framework.filters import SearchFilter
from rest_framework.generics import CreateAPIView, RetrieveUpdateAPIView
from rest_framework.mixins import (CreateModelMixin, DestroyModelMixin,
                                   ListModelMixin)
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.views import Response, status
from rest_framework.viewsets import GenericViewSet, ModelViewSet

from .filters import TitleFilterBackend
from .models import Categories, Comments, Genres, Reviews, Titles
from .permissions import IsAdmin, IsModerator, IsOwnerOrReadOnly, ReadOnly
from .serializers import (CategorySerializer, CommentsSerializer,
                          CreateUserSerializer, GenreSerializer,
                          ReviewsSerializer, TitleSerializerRead,
                          TitleSerializerWrite, UserSerializer)

User = get_user_model()


class CreateListDestroyView(CreateModelMixin, ListModelMixin,
                            DestroyModelMixin, GenericViewSet):
    pass


class CreateUser(CreateAPIView):
    permission_classes = [AllowAny]

    def post(self, request):
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
                message='Код подтверждения - {}'.format(confirmation_code),
                from_email='Test@test.com'
            )
            return Response(serialized.data, status=status.HTTP_201_CREATED)
        return Response(serialized.errors, status=status.HTTP_400_BAD_REQUEST)


class UsersListCreateViewSet(ModelViewSet):
    lookup_field = 'username'
    queryset = User.objects.all().order_by('-id')
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated, IsAdmin]
    filter_backends = [SearchFilter]
    search_fields = ('username',)


class UserPersonalData(RetrieveUpdateAPIView):
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return self.request.user


class ReviewsViewSet(ModelViewSet):
    serializer_class = ReviewsSerializer
    permission_classes = [IsOwnerOrReadOnly | IsAdmin | IsModerator]

    def get_queryset(self):
        title_id = self.kwargs['title_id']
        title = get_object_or_404(Titles, id=title_id)
        queryset = Reviews.objects.filter(title=title).order_by('-pub_date')
        return queryset

    def perform_create(self, serializer):
        title = get_object_or_404(Titles, pk=self.kwargs.get('title_id'))
        is_unqiue = Reviews.objects.filter(
            author=self.request.user,
            title=title
        ).exists()
        if is_unqiue:
            raise ValidationError('You can write only one review.')
        serializer.save(author=self.request.user, title=title)


class CommentsViewSet(ModelViewSet):
    serializer_class = CommentsSerializer
    permission_classes = [IsOwnerOrReadOnly | IsAdmin | IsModerator]
    pagination_class = PageNumberPagination

    def get_queryset(self):
        title_id = self.kwargs['title_id']
        title = get_object_or_404(Titles, id=title_id)
        review_id = self.kwargs['review_id']
        review = get_object_or_404(Reviews, title=title, id=review_id)
        queryset = Comments.objects.filter(review=review).order_by('-pub_date')
        return queryset

    def perform_create(self, serializer):
        review = get_object_or_404(Reviews, pk=self.kwargs.get('review_id'))
        serializer.save(author=self.request.user, review=review)


class CategoryViewSet(CreateListDestroyView):
    queryset = Categories.objects.all().order_by('-name')
    permission_classes = [ReadOnly | IsAdmin]
    serializer_class = CategorySerializer
    lookup_field = 'slug'
    filter_backends = [SearchFilter]
    search_fields = ['=name', '=slug']


class GenreViewSet(CreateListDestroyView):
    queryset = Genres.objects.all().order_by('-name')
    permission_classes = [ReadOnly | IsAdmin]
    serializer_class = GenreSerializer
    lookup_field = 'slug'
    filter_backends = [SearchFilter]
    search_fields = ['=name']


class TitleViewSet(ModelViewSet):
    queryset = Titles.objects.all().order_by('-name')
    permission_classes = [ReadOnly | IsAdmin]
    filter_backends = [TitleFilterBackend]

    def get_serializer_class(self):
        if self.request.method in permissions.SAFE_METHODS:
            return TitleSerializerRead
        return TitleSerializerWrite
