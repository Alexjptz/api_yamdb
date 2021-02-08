from django.contrib.auth import get_user_model
from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

from .models import Categories, Comments, Genres, Reviews, Titles

User = get_user_model()


class CreateUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('email',)


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            'first_name',
            'last_name',
            'username',
            'bio',
            'email',
            'role',
        )


class GetMyTokenSerializer(TokenObtainPairSerializer):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        del self.fields['password']
        self.fields['confirmation_code'] = serializers.CharField(
            required=True
        )

    def validate(self, attrs):
        attrs['password'] = attrs.pop('confirmation_code')
        return super().validate(attrs)


class ReviewsSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        slug_field='username',
        read_only=True
    )

    class Meta:
        fields = ('id', 'text', 'author', 'score', 'pub_date',)
        model = Reviews


class CommentsSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        slug_field='username',
        read_only=True
    )

    class Meta:
        fields = ('id', 'text', 'author', 'pub_date',)
        model = Comments


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        fields = ('name', 'slug',)
        model = Categories


class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        fields = ('name', 'slug',)
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
        many=True,
        slug_field='slug',
        queryset=Genres.objects.all()
    )
    category = serializers.SlugRelatedField(
        slug_field='slug',
        required=False,
        queryset=Categories.objects.all()
    )

    class Meta:
        fields = '__all__'
        model = Titles
