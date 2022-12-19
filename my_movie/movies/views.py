from django.shortcuts import render, redirect
from .models import Movie, Actor, Genre
from django.views.generic.base import View
from django.views.generic import ListView, DetailView
from .forms import ReviewsForm
from django.db.models import Q

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



class MovieDetailView(GenreYear, DetailView):
    '''Полное описание фильма'''
    model = Movie
    slug_field = 'url'
    context_object_name = 'movie'
    
class AddReview(View):
    """Отправка отзывов"""
    def post(self, request, pk):
        movie = Movie.objects.get(id=pk)
        form = ReviewsForm(request.POST)
        if form.is_valid():
            form = form.save(commit = False)
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
    def get_queryset(self):
        genres_from_GET = self.request.GET.getlist('genre')
        years_from_GET = self.request.GET.getlist('year')
        
        by_genres = Q(genres__in = genres_from_GET)
        by_years = Q(year__in = years_from_GET)
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
        
