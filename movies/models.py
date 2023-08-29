from django.db import models
from datetime import date

from django.urls import reverse


class Category(models.Model):
    """Категории"""
    name = models.CharField('Категория', max_length=150)
    description = models.TextField('Описание')
    url = models.SlugField(max_length=150, unique=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'


class Actor(models.Model):
    """Актеры и режисеры"""
    name = models.CharField('Имя', max_length=100)
    age = models.PositiveSmallIntegerField('Возраст', default=0)
    description = models.TextField('Описание')
    image = models.ImageField('Изображение', upload_to='actors/')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Актеры и режисеры'
        verbose_name_plural = 'Актеры и режисеры'

    def get_absolute_url(self):
        return reverse("actor_detail", kwargs={"slug": self.name})


class Genres(models.Model):
    """Жанры"""
    name = models.CharField('Имя', max_length=100)
    description = models.TextField('Описание')
    url = models.SlugField(max_length=150, unique=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Жанр'
        verbose_name_plural = 'Жанры'


class Movie(models.Model):
    """Фильм"""
    title = models.CharField('Имя', max_length=100)
    tagline = models.CharField('Слоган', max_length=200, default='')
    description = models.TextField('Описание')
    poster = models.ImageField('Постер', upload_to='movies/')
    year = models.PositiveSmallIntegerField('Дата выхода', default=2022)
    country = models.CharField('Страна', max_length=100)
    directors = models.ManyToManyField(Actor, verbose_name='Режисер', related_name='film_director')
    actors = models.ManyToManyField(Actor, verbose_name='Актеры', related_name='film_actor')
    genres = models.ManyToManyField(Genres, verbose_name='Жарны')
    world_premier = models.DateField('Премьера в мире', default=date.today)
    budget = models.PositiveSmallIntegerField('Бюджет', default=0,
                                              help_text='Указывать сумму в долларах'
                                              )
    fees_in_usa = models.PositiveSmallIntegerField('Сборы в США', default=0,
                                                   help_text='Указывать сумму в долларах'
                                                   )
    fees_in_world = models.PositiveSmallIntegerField('Сборы в мире', default=0,
                                                     help_text='Указывать сумму в долларах'
                                                     )
    category = models.ForeignKey(Category, verbose_name='Категория', on_delete=models.SET_NULL, null=True)
    url = models.SlugField(max_length=160, unique=True)
    draft = models.BooleanField('Черновик', default=False)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("movie_detail", kwargs={"slug": self.url})

    def get_review(self):
        return self.revive_set.filter(perent__isnull=True)

    class Meta:
        verbose_name = 'Фильм'
        verbose_name_plural = 'Фильмы'


class MoviesShots(models.Model):
    """Кадры из фильма"""
    title = models.CharField('Заголовок', max_length=150)
    description = models.TextField('Описание')
    image = models.ImageField('Изображение', upload_to='movie_shots/')
    movie = models.ForeignKey(Movie, verbose_name='Фильм', on_delete=models.CASCADE)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Кадр из фильма'
        verbose_name_plural = 'Кадры из фильма'


class RatingStars(models.Model):
    """Звезды рейтинга"""
    value = models.SmallIntegerField('Значение', default=0)

    def __str__(self):
        return f'{self.value}'

    class Meta:
        verbose_name = 'Звезда рейтинга'
        verbose_name_plural = 'Зыезды рейтинга'
        ordering = ['-value']


class Rating(models.Model):
    """Рейтинг"""
    ip = models.CharField('IP адрес', max_length=15)
    star = models.ForeignKey(RatingStars, verbose_name='Звезда', on_delete=models.CASCADE)
    movie = models.ForeignKey(Movie, verbose_name='Фильм', on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.star} - {self.movie}'

    class Meta:
        verbose_name = 'Рэйтинг'
        verbose_name_plural = 'Рэйтинги'


class Revive(models.Model):
    """Отзывы"""
    email = models.EmailField()
    name = models.CharField('Имя', max_length=100)
    text = models.TextField('Текст', max_length=5000)
    perent = models.ForeignKey(
        'self', verbose_name='Родитель', on_delete=models.SET_NULL, null=True, blank=True
    )
    movie = models.ForeignKey(Movie, verbose_name='Фильм', on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.name} - {self.movie}'

    class Meta:
        verbose_name = 'Отзыв'
        verbose_name_plural = 'Отзывы'