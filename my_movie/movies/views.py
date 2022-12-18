from django.shortcuts import render, redirect
from .models import Movie, Actor 
from django.views.generic.base import View
from django.views.generic import ListView, DetailView
from .forms import ReviewsForm

class MoviesView(ListView):
    '''Список фильмов'''
    context_object_name = 'movie_list'
    model = Movie
    queryset = Movie.objects.filter(draft=False)


class MovieDetailView(DetailView):
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
class ActorView(DetailView):
    model = Actor
    template_name = 'movies/actor.html'
    slug_field = 'name'
    context_object_name = 'actor'
