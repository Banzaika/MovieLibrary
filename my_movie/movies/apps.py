from django.apps import AppConfig


class MoviesConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'movies'
    verbose_name = "Фильм"
    verbose_name_plural = "Фильмы"
