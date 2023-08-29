from modeltranslation.translator import register, TranslationOptions
from .models import Category, Actor, Movie, Genres, MoviesShots


@register(Category)
class CategoryTranslationOptions(TranslationOptions):
    fields = ('name', 'description')


@register(Actor)
class ActorTranslationOptions(TranslationOptions):
    fields = ('name', 'description')


@register(Genres)
class GenreTranslationOptions(TranslationOptions):
    fields = ('name', 'description')


@register(Movie)
class MovieTranslationOptions(TranslationOptions):
    fields = ('title', 'tagline', 'description', 'country')


@register(MoviesShots)
class MovieShotsTranslationOptions(TranslationOptions):
    fields = ('title', 'description')