from django.db.models import *
from datetime import date
from django.urls import reverse

class Category(Model):
    '''Категории'''
    name = CharField("Категория", max_length=50)
    description = TextField("Описание")
    url = SlugField(max_length=160, unique=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Категория"
        verbose_name_plural = "Категории"


class Actor(Model):
    '''Актеры и режиссеры'''
    name = CharField("Имя", max_length=150)
    age = PositiveSmallIntegerField("Возраст", default=0)
    description = TextField("Описание")
    image = ImageField("Изображение", upload_to="actors/")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Актеры и Режиссеры"
        verbose_name_plural = "Актеры и Режиссеры"
    
    def get_absolute_url(self):
        return reverse('movies:actor_detail', kwargs={'slug': self.name})


class Genre(Model):
    name = CharField("Название", max_length=50)
    description = TextField("Описание")
    url = SlugField(max_length=160, unique=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Жанр"
        verbose_name_plural = "Жанры"


class Movie(Model):
    '''Фильм'''
    title = CharField("Название", max_length=50)
    tagline = CharField("Слоган", max_length=100, default='')
    description = TextField("Описание")
    poster = ImageField("Постер", upload_to="movies/")
    year = PositiveSmallIntegerField("Возраст", default=2019)
    country = CharField('Страна', max_length=20)
    directors = ManyToManyField(
        Actor, verbose_name='режиссеры', related_name='film_director')
    actors = ManyToManyField(
        Actor, verbose_name='Актеры', related_name='film_actor')
    genres = ManyToManyField(Genre, verbose_name='Жанры')
    world_premiere = PositiveIntegerField(
        "Премьера в мире", default=date.today())
    budget = PositiveIntegerField(
        "Бюджет", default=0, help_text="указывать сумму в долларах")
    fees_in_usa = PositiveIntegerField(
        "Сборы в NoneСША", default=0, help_text="указывать сумму в долларах")
    fees_in_world = PositiveIntegerField(
        "Сборы в мире", default=0, help_text="указывать сумму в долларах")
    category = ForeignKey(Category, verbose_name="Категория",
                          on_delete=SET_NULL, null=True)
    url = SlugField(max_length=130, unique=True)
    draft = BooleanField("Черновик", default=False)

    def __str__(self):
        return self.title

    def get_parent_reviews(self):
        return self.reviews_set.filter(parent__isnull = True)

    def get_absolute_url(self):
        return reverse('movies:movie_detail', kwargs={"slug": self.url})

    class Meta:
        verbose_name = "Фильм"
        verbose_name_plural = "Фильмы"


class MovieShots(Model):
    '''Звезды рейтинга'''
    title = CharField("Название", max_length=100)
    description = TextField("Описание")
    image = ImageField("Изображение", upload_to="movie_shots/")
    movie = ForeignKey(Movie, verbose_name="Фильм", on_delete=CASCADE)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "Кадр из Фильма"
        verbose_name_plural = "Кадры из Фильма"


class RatingStar(Model):
    value = PositiveSmallIntegerField("Значение", default=0)

    def __str__(self):
        return self.value

    class Meta:
        verbose_name = "Звезда рейтинга"
        verbose_name_plural = "Звезды рейтинга"


class Rating(Model):
    '''Рейтинг'''
    ip = CharField("IP адрес", max_length=15)
    star = ForeignKey(RatingStar, on_delete=CASCADE, verbose_name="звезда")
    movie = ForeignKey(Movie, verbose_name="Фильм", on_delete=CASCADE)

    def __str__(self):
        return f"{self.star} - {self.movie}"

    class Meta:
        verbose_name = "Рейтинг"
        verbose_name_plural = "Рейтинги"


class Reviews(Model):
    email = EmailField()
    name = CharField("Имя", max_length=100)
    text = TextField("Сообщение", max_length=5000)
    parent = ForeignKey('self', verbose_name='Родитель',
                        blank=True, null=True, on_delete=SET_NULL)
    movie = ForeignKey(Movie, verbose_name="Фильм", on_delete=CASCADE)

    def __str__(self):
        return f'{self.name} - {self.movie}'

    class Meta:
        verbose_name = "Отзыв"
        verbose_name_plural = "Отзывы"
