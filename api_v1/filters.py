from rest_framework import filters


class TitleFilterBackend(filters.BaseFilterBackend):
    def filter_queryset(self, request, queryset, view):
        description = request.GET.get('description')
        category = request.GET.get('category')
        genre = request.GET.get('genre')
        name = request.GET.get('name')
        year = request.GET.get('year')
        if category is not None:
            queryset = queryset.filter(category__slug=category)
        if genre is not None:
            queryset = queryset.filter(genre__slug=genre)
        if name is not None:
            queryset = queryset.filter(name__contains=name)
        if description is not None:
            queryset = queryset.filter(description_contains=description)
        if year is not None:
            queryset = queryset.filter(year=year)
        return queryset
