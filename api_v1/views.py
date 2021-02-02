from re import split

from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
from rest_framework import permissions
from rest_framework.exceptions import ValidationError
from rest_framework.filters import SearchFilter
from rest_framework.generics import CreateAPIView, RetrieveUpdateAPIView
from rest_framework.mixins import (CreateModelMixin, DestroyModelMixin,
                                   ListModelMixin, UpdateModelMixin)
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import (AllowAny, IsAuthenticated,
                                        IsAuthenticatedOrReadOnly)
from rest_framework.views import APIView, Response, status
from rest_framework.viewsets import GenericViewSet, ModelViewSet

from .models import Categories, Comments, Genres, Reviews, Titles
from .permissions import IsAdmin, IsModerator, IsOwnerOrReadOnly
from .serializers import (CategorySerializer, CommentsSerializer,
                          CreateUserSerializer, GenreSerializer,
                          ReviewsSerializer, TitleSerializerRead,
                          TitleSerializerWrite, UserSerializer)

User = get_user_model()


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
                message='Твой код подтверждения - {}'.format(confirmation_code),
                from_email='Test@test.com'
            )
            return Response(serialized.data, status=status.HTTP_201_CREATED)
        return Response(serialized.errors, status=status.HTTP_400_BAD_REQUEST)


# @api_view(['POST'])
# @permission_classes([AllowAny])
# def create_user(request):
#     serialized = CreateUserSerializer(data=request.data)
#     if serialized.is_valid():
#         confirmation_code = User.objects.make_random_password()
#         username = split(r'@', serialized.data['email'])[0]
#         user = User.objects.create_user(
#             email=serialized.data['email'],
#             username=username,
#             password=confirmation_code
#         )
#         user.email_user(
#             subject='Код подтверждения',
#             message='Твой код подтверждения - {}'.format(confirmation_code),
#             from_email='Test@test.com'
#         )
#         return Response(serialized.data, status=status.HTTP_201_CREATED)
#     return Response(serialized.errors, status=status.HTTP_400_BAD_REQUEST)


class UsersListCreateViewSet(CreateModelMixin, ListModelMixin, GenericViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated, IsAdmin]
    filter_backends = [SearchFilter]
    search_fields = ('username',)
    pagination_class = PageNumberPagination


class UserPersonalData(ListModelMixin, UpdateModelMixin, GenericViewSet):
    serializer_class = UserSerializer
    permissions_classes = [IsAuthenticated, IsOwnerOrReadOnly]

    def get_object(self):
        obj = get_object_or_404(g)
        return 

    def get_queryset(self):
        queryset = User.objects.filter(username=self.request.user)
        return queryset

    def perform_update(self, serializer):
        serializer.save()


class UserAdminViewSet(CreateModelMixin, ListModelMixin, GenericViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated, IsAdmin]


class ReviewsViewSet(ModelViewSet):
    serializer_class = ReviewsSerializer
    permission_classes = [IsAuthenticated, IsOwnerOrReadOnly]

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


class CommentsViewSet(ModelViewSet):
    serializer_class = CommentsSerializer
    permission_classes = [IsOwnerOrReadOnly]
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


class CategoryViewSet(ModelViewSet):
    permission_classes = [IsOwnerOrReadOnly]
    serializer_class = CategorySerializer
    queryset = Categories.objects.all()
    http_method_names = ['get', 'post', 'delete']
    lookup_field = 'slug'
    filter_backends = [SearchFilter]
    search_fields = ['=name']


class GenreViewSet(ModelViewSet):
    queryset = Genres.objects.all()
    permission_classes = [IsOwnerOrReadOnly]
    serializer_class = GenreSerializer
    http_method_names = ['get', 'post', 'delete']
    lookup_field = 'slug'
    filter_backends = [SearchFilter]
    search_fields = ['=name']


class TitleViewSet(ModelViewSet):
    queryset = Titles.objects.all()
    permission_classes = [IsOwnerOrReadOnly]
    filter_backends = [SearchFilter]
    search_fields = ['=name', '=year', '=category__slug', '=genre__slug']

    def get_serializer_class(self):
        if self.request.method in permissions.SAFE_METHODS:
            return TitleSerializerRead
        return TitleSerializerWrite
