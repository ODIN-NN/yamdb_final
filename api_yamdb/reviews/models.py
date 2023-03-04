import datetime as dt

from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from users.models import User


class Category(models.Model):
    name = models.TextField(
        db_index=True,
        max_length=256,
        verbose_name='Название категории',
    )
    slug = models.SlugField(
        unique=True,
        max_length=50,
    )

    class Meta:
        verbose_name = 'Категория',
        verbose_name_plural = 'Категории'


class Title(models.Model):
    name = models.TextField(
        db_index=True,
        max_length=256,
        verbose_name='Название произедения',
    )
    year = models.IntegerField(
        validators=[
            MaxValueValidator(dt.date.today().year),
            MinValueValidator(-4000),
        ]
    )
    description = models.TextField(
        null=True,
        blank=True
    )
    category = models.ForeignKey(
        Category,
        db_index=True,
        on_delete=models.CASCADE,
        related_name='titles'
    )

    def genre(self):
        return self.genre_set.all()

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Произведение',
        verbose_name_plural = 'Произведения'


class Genre(models.Model):
    name = models.TextField(
        db_index=True,
        max_length=256,
        verbose_name='Название жанра'
    )
    slug = models.SlugField(unique=True)
    title = models.ManyToManyField(
        Title,
        db_index=True,
        related_name='genre'
    )

    def __str__(self):
        return f"{{'name': {self.name}, 'slug': {self.slug}}}"

    class Meta:
        verbose_name = 'Жанр',
        verbose_name_plural = 'Жанры'


class Review(models.Model):
    title = models.ForeignKey(Title, on_delete=models.CASCADE,
                              related_name='reviews')
    text = models.TextField()
    author = models.ForeignKey(User, on_delete=models.CASCADE,
                               related_name='reviews')
    score = models.IntegerField(default=0,
                                blank=True,
                                verbose_name='Рейтинг',
                                validators=[
                                    MaxValueValidator(10),
                                    MinValueValidator(1)
                                ])
    pub_date = models.DateTimeField(
        'Дата добавления', auto_now_add=True, db_index=True)

    class Meta:
        unique_together = ('title', 'author')

    def __str__(self):
        return f'Отзыв о произведении {self.title_id.name}'


class Comment(models.Model):
    review = models.ForeignKey(Review, on_delete=models.CASCADE,
                               related_name='comments')
    text = models.TextField()
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='comments',
    )
    pub_date = models.DateTimeField(
        'Дата добавления',
        auto_now_add=True,
        db_index=True,
    )
