from django.contrib import messages
from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse
from django.shortcuts import render
from django.views.generic import ListView, DetailView
from django.views import View
from taggit.models import Tag
from movies.models import Movie
from movies.forms import RateMovieForm, ReviewMovieForm


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


class ReviewRateMovieBaseClass(View):
    form_class = None
    template_name = ''
    success_message = ''
    nonexistent_template = 'movies/nonexistent.html'

    def get_object(self, request, pk):
        print('get object')
        obj = Movie.objects.filter(pk=pk).first()
        return obj

    def get(self, request, *args, **kwargs):
        movie = self.get_object(request, self.kwargs['pk'])
        if not movie:
            return render(request, self.nonexistent_template)
        form = self.form_class()
        return render(request, self.template_name, {'form': form, 'movie_pk': movie.id})

    def post(self, request, **kwargs):
        movie = self.get_object(request, kwargs['pk'])
        if not movie:
            return render(request, self.nonexistent_template)
        form = self.form_class(request.POST)
        if form.is_valid():
            form.instance.movie = movie
            form.instance.owner = request.user
            form.save()
            messages.success(request, self.success_message)
            return HttpResponseRedirect(reverse('movies:movie-detail', args=(kwargs['pk'], )))
        return render(request, self.template_name, {'form': form, 'movie_pk': movie.id})


class ReviewMovieView(ReviewRateMovieBaseClass):
    form_class = ReviewMovieForm
    template_name = 'movies/review_movie.html'
    success_message = 'You successfully reviewed a movie'


class RateMovieView(ReviewRateMovieBaseClass):
    form_class = RateMovieForm
    template_name = 'movies/rate_movie.html'
    success_message = 'You successfully rated a movie'
