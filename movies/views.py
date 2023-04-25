from django.shortcuts import render
from django.views.generic import ListView, DetailView
from django.views.generic.detail import SingleObjectMixin
from django.views import View
from taggit.models import Tag
from movies.models import Movie


class MoviesByGenre(ListView):
    model = Movie
    context_object_name = 'movies'
    template_name = "movies/movies_by_genre.html"

    def get_queryset(self):
        genre = self.kwargs['genre']
        genre_object = Tag.objects.filter(slug=genre).first()
        movies = Movie.objects.prefetch_related(
            'genres').filter(genres=genre_object).order_by('-release_date').all()
        return movies

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['genre'] = ' '.join(self.kwargs['genre'].split('-'))
        return context


class MovieDetailView(View):
    def get(self, request, *args, **kwargs):
        movie = Movie.objects.prefetch_related(
            'genres').filter(pk=kwargs['pk']).first()
        if not movie:
            return render(request, 'movies/nonexistent.html')
        return render(request, 'movies/movie_detail.html', {'movie': movie})
