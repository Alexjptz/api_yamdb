from api_v1.models import Categories, Genres, Titels
from rest_framework import serializers


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
        model = Titels


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
        model = Titels
        