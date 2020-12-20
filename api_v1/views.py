from rest_framework import filters, viewsets, permissions

from .permissions import IsAdminOrSafeMethod
from .models import Titels, Categories, Genres
from .serializers import (
    TitleSerializerRead, 
    TitleSerializerWrite,
    GenreSerializer,
    CategorySerializer
)



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
    queryset = Titels.objects.all()
    permission_classes = [IsAdminOrSafeMethod]
    filter_backends = (filters.SearchFilter)
    search_fields = ['=name', '=year', '=category__slug', '=genre__slug']    

    def get_serializer_class(self):
        if self.request.method in permissions.SAFE_METHODS:
            return TitleSerializerRead
        return TitleSerializerWrite
