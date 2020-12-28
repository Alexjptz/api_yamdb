from rest_framework import serializers
<<<<<<< HEAD

from .models import Categories, Comments, Genres, Reviews, Titles
=======
from .models import Comments, Reviews
>>>>>>> 120604420271fc9c1a3fb8c9f3cc4b78b10dfe01


class ReviewsSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        slug_field='username',
        read_only=True
    )

    class Meta:
        fields = ('id', 'text', 'author', 'score', 'pub_date')
        model = Reviews


class CommentsSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        slug_field='username',
        read_only=True
    )

    class Meta:
        fields = ('id', 'text', 'author', 'pub_date')
        model = Comments


<<<<<<< HEAD
=======
from api_v1.models import Categories, Genres, Titles
from rest_framework import serializers


>>>>>>> 120604420271fc9c1a3fb8c9f3cc4b78b10dfe01
class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        fields = ['name', 'slug']
        model = Categories


class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        fields = ['name', 'slug']
        model = Genres


class TitleSerializerRead(serializers.ModelSerializer):
    genre = GenreSerializer(many=True, required=False)
    category = CategorySerializer(required=False)
    rating = serializers.IntegerField(required=False)

    class Meta:
        fields = '__all__'
        model = Titles


class TitleSerializerWrite(serializers.ModelSerializer):
    rating = serializers.IntegerField(required=False)
    genre = serializers.SlugRelatedField(
        many=True, slug_field='slug', queryset=Genres.objects.all()
    )
    category = serializers.SlugRelatedField(
        slug_field='slug', required=False, queryset=Categories.objects.all()
    )

    class Meta:
        fields = '__all__'
        model = Titles
