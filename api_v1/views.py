from django.shortcuts import get_object_or_404
from rest_framework import filters, permissions, viewsets
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAuthenticatedOrReadOnly

from .models import Categories, Comments, Genres, Reviews, Titles
from .permissions import IsAdminOrSafeMethod, IsOwnerOrAdminOrReadOnly
from .serializers import (CategorySerializer, CommentsSerializer,
                          GenreSerializer, ReviewsSerializer,
                          TitleSerializerRead, TitleSerializerWrite)


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


class CategoryViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAdminOrSafeMethod]
    serializer_class = CategorySerializer
    queryset = Categories.objects.all()
    http_method_names = ['get', 'post', 'delete']
    lookup_field = 'slug'
    filter_backends = [filters.SearchFilter]
    search_fields = ['=name']


class GenreViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAdminOrSafeMethod]
    serializer_class = GenreSerializer
    queryset = Genres.objects.all()
    http_method_names = ['get', 'post', 'delete']
    lookup_field = 'slug'
    filter_backends = [filters.SearchFilter]
    search_fields = ['=name']


class TitleViewSet(viewsets.ModelViewSet):
    queryset = Titles.objects.all()
    permission_classes = [IsAdminOrSafeMethod]
    filter_backends = (filters.SearchFilter)
    search_fields = ['=name', '=year', '=category__slug', '=genre__slug']

    def get_serializer_class(self):
        if self.request.method in permissions.SAFE_METHODS:
            return TitleSerializerRead
        return TitleSerializerWrite
