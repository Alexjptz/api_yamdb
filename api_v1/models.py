from django.contrib.auth import get_user_model
from django.db import models
from django.db.models.deletion import SET_NULL
from django.db.models.fields import IntegerField

from django.utils.text import slugify

User = get_user_model()


def get_unique_slug(self, model):
    slug = slugify(self.name)
    unique_slug = slug
    num = 1
    while model.objects.filter(slug=unique_slug).exists():
        unique_slug = '{}-{}'.format(slug, num)
        num += 1
    return unique_slug


class Categories(models.Model):
    name = models.CharField('Название категории', max_length=50)
    slug = models.SlugField(
        'URL путь', unique=True, max_length=50, blank=True, null=True
    )

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = get_unique_slug(self, Categories)
        super().save(*args, **kwargs)


class Genres(models.Model):
    name = models.CharField('Название жанра', max_length=50)
    slug = models.SlugField(
        'URL путь', unique=True, max_length=99, blank=True, null=True
    )

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = get_unique_slug(self, Genres)
        super().save(*args, **kwargs)


class Titels(models.Model):
    name = models.CharField(max_length=50, blank=False, null=False)
    year = models.PositiveSmallIntegerField(
        blank=True, null=True, db_index=True
    )
    rating = models.IntegerField()                    # тут непонятно как сделать
    description = models.TextField(blank=True, null=True)
    genre = models.ManyToManyField(Genres, db_index=True)
    category = models.ForeignKey(
        Categories,
        related_name='titles',
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        db_index=True
    )

    def __str__(self):
        return self.name


class Rewiews(models.Model):
    pass


class Comments(models.Model):
    pass
