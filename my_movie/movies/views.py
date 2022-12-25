from django.shortcuts import render, redirect
from .models import Movie, Actor, Genre, Rating
from django.views.generic.base import View
from django.views.generic import ListView, DetailView
from .forms import ReviewsForm, RatingForm
from django.db.models import Q
from django.http import HttpResponse


class GenreYear:
    def get_years(self):
        return Movie.objects.filter(draft=False).distinct('year').values('year')

    def get_genres(self):
        return Genre.objects.all()


class MoviesView(GenreYear, ListView):
    '''Список фильмов'''
    context_object_name = 'movie_list'
    model = Movie
    queryset = Movie.objects.filter(draft=False)
    paginate_by = 1


class MovieDetailView(GenreYear, DetailView):
    '''Полное описание фильма'''
    model = Movie
    slug_field = 'url'
    context_object_name = 'movie'

    def get_context_data(self, **kwargs):
        context = super(MovieDetailView, self).get_context_data(**kwargs)
        context['rating_form'] = RatingForm()
        return context


class AddReview(View):
    """Отправка отзывов"""

    def post(self, request, pk):
        movie = Movie.objects.get(id=pk)
        form = ReviewsForm(request.POST)
        if form.is_valid():
            form = form.save(commit=False)
            if request.POST.get('parent', None):
                form.parent_id = int(request.POST.get('parent'))
            form.movie = movie
            form.save()
            return redirect(movie.get_absolute_url())


class ActorView(GenreYear, DetailView):
    model = Actor
    template_name = 'movies/actor.html'
    slug_field = 'name'
    context_object_name = 'actor'


class FilterMovie(GenreYear, ListView):
    """Фильтр фильмов по годам выпуска и жанрам"""
    paginate_by = 1
    def get_queryset(self):
        genres_from_GET = self.request.GET.getlist('genre')
        years_from_GET = self.request.GET.getlist('year')

        by_genres = Q(genres__in=genres_from_GET)
        by_years = Q(year__in=years_from_GET)
        # queryset = Movie.objects.filter(by_genres | by_years)
        # return queryset
        if genres_from_GET and years_from_GET:
            queryset = Movie.objects.filter(by_genres, by_years)
            return queryset

        elif genres_from_GET and not years_from_GET:
            queryset = Movie.objects.filter(by_genres)
            return queryset

        elif not genres_from_GET and years_from_GET:
            queryset = Movie.objects.filter(by_years)
            return queryset

        else:
            return Movie.objects.none()

    def get_context_data(self, **kwargs):
        context = super().get_context_data( **kwargs)
        context['year'] = ''.join([f"year={x}&" for x in self.request.GET.getlist('year')])
        context['genre'] = ''.join([f"genre={x}&" for x in self.request.GET.getlist('genre')])
        return context


class AddStarRating(View):
    def get_ip(self, request):
        x_forward_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forward_for:
            ip = x_forward_for.split(',')[0]
        else:
            ip = request.META.get('REMOTE_ADDR')
        return ip
    
    def post(self, request):
        form = RatingForm(request.POST)
        if form.is_valid():
            print(request)
            Rating.objects.update_or_create(
                ip=self.get_ip(request),
                movie_id=int(request.POST.get('movie')),
                defaults={"star_id": int(request.POST.get("star"))}
            )
            return HttpResponse(status=200)
        else:
            return HttpResponse(status=400)