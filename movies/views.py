from django.views.generic import ListView
from movies.models import Movie


class MovieListView(ListView):
    model = Movie
    context_object_name = 'movies'
