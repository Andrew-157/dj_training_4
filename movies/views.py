from django.http import HttpResponseRedirect
from django.urls import reverse
from django.shortcuts import render
from django.views.generic import ListView, DetailView
from django.views import View
from taggit.models import Tag
from movies.models import Movie
from movies.forms import RateMovieForm


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


class MovieDetailView(DetailView):
    model = Movie
    template_name = 'movies/movie_detail.html'
    queryset = Movie.objects.prefetch_related('genres').all()
    context_object_name = 'movie'

    def get_object(self):
        movie_pk = self.kwargs['pk']
        movie = Movie.objects.filter(pk=movie_pk).first()
        if not movie:
            return None
        return super().get_object()


class RateMovieView(View):
    form_class = RateMovieForm
    template_name = 'movies/rate_movie.html'

    def get_object(self, request, pk):
        movie = Movie.objects.filter(pk=pk).first()
        if not movie:
            return render(request, 'movies/nonexistent.html')
        return movie

    def get(self, request, *args, **kwargs):
        movie = self.get_object(request, self.kwargs['pk'])
        form = self.form_class()
        return render(request, self.template_name, {'form': form, 'movie': movie})

    def post(self, request, **kwargs):
        movie = self.get_object(request, kwargs['pk'])
        form = self.form_class(request.POST)
        if form.is_valid():
            form.instance.movie = movie
            form.instance.rated_by = request.user
            form.save()
            return HttpResponseRedirect(reverse('movies:movie-detail', args=(kwargs['pk'], )))
        return render(request, self.template_name, {'form': form, 'movie': movie})
