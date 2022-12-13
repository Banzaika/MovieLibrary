from django.shortcuts import render
from .models import Movie
from django.views.generic.base import View

class MoviesView(View):
    def get(self, request):
        movies = Movie.objects.all()
        return render(request, 'movies/movie_list.html', {'movie_list': movies})
