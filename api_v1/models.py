from django.contrib.auth import get_user_model
from django.db import models
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


class Titles(models.Model):
    name = models.CharField(max_length=50, blank=False, null=False)
    year = models.PositiveSmallIntegerField(
        blank=True, null=True, db_index=True
    )
    rating = models.IntegerField()  # тут непонятно как сделать
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


class Reviews(models.Model):
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='reviews'
    )
    title = models.ForeignKey(
        Titles,
        on_delete=models.CASCADE,
        related_name='reviews'
    )
    text = models.TextField()
    score_choices = [(i, i) for i in range(1, 11)]
    score = models.IntegerField(choices=score_choices)
    pub_date = models.DateTimeField(
        'Дата добавления',
        auto_now_add=True,
        db_index=True
    )


class Comments(models.Model):
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='comments'
    )
    review = models.ForeignKey(
        Reviews,
        on_delete=models.CASCADE,
        related_name='comments'
    )
    text = models.TextField()
    pub_date = models.DateTimeField(
        'Дата добавления',
        auto_now_add=True,
        db_index=True
    )
