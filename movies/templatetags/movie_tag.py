from django import template
from movies.models import Category, Movie

register = template.Library()


@register.simple_tag()
def get_categories():
    """Вывод всех категорий"""
    return Category.objects.all()


@register.inclusion_tag('movies/tags/last_movie.html')
def get_last_movie(count=5):
    """Вывод последний фильмов"""
    movies = Movie.objects.filter(draft=False).order_by('id').reverse()[:count]
    return {'last_movies': movies}
