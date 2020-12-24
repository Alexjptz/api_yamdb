# from django.contrib.auth import get_user_model
from django.db import models
from users.models import User

# User = get_user_model()


class Categories(models.Model):
    pass


class Genres(models.Model):
    pass


class Titles(models.Model):
    pass


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
