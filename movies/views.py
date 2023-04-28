from typing import Any, Dict
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.utils.decorators import method_decorator
from django.shortcuts import render, redirect
from django.views.generic import ListView, DetailView
from django.views import View
from taggit.models import Tag
from movies.models import Movie, Review
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


class ReviewsByMovieList(ListView):
    model = Review
    context_object_name = 'reviews'
    template_name = "movies/reviews_by_movie.html"
    valid_movie_pk = True

    def get_queryset(self):
        pk = self.kwargs['pk']
        movie = Movie.objects.filter(pk=pk).first()
        if not movie:
            self.valid_movie_pk = False
            self.template_name = 'movies/nonexistent.html'
            return None
        reviews = Review.objects.select_related('owner').\
            order_by('-pub_date').filter(pk=pk).all()
        self.kwargs['movie'] = movie
        return reviews

    def get_context_data(self, **kwargs: Any):
        context = super().get_context_data(**kwargs)
        # variable valid_movie_pk lets us know if pk provided in url is valid
        # if it is not, then we return context as it was because we are gonna show
        # that the resource does not exist
        if not self.valid_movie_pk:
            return context
        else:
            context['movie'] = self.kwargs['movie']
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
            self.template_name = 'movies/nonexistent.html'
            return None
        return super().get_object()


class ReviewRateMovieBaseClass(View):
    form_class = None
    template_name = ''
    success_message = ''
    info_message = ''
    nonexistent_template = 'movies/nonexistent.html'
    redirect_to = ''

    def get_object(self, pk):
        obj = Movie.objects.filter(pk=pk).first()
        return obj

    def get(self, request, *args, **kwargs):
        current_user = request.user
        movie = self.get_object(self.kwargs['pk'])
        if not movie:
            return render(request, self.nonexistent_template)
        if not current_user.is_authenticated:
            messages.info(request, self.info_message)
            return HttpResponseRedirect(reverse(self.redirect_to, args=(movie.id, )))
        form = self.form_class()
        return render(request, self.template_name, {'form': form, 'movie_pk': movie.id})

    def post(self, request, **kwargs):
        current_user = request.user
        movie = self.get_object(kwargs['pk'])
        if not movie:
            return render(request, self.nonexistent_template)
        if not current_user.is_authenticated:
            messages.info(request, self.info_message)
            return HttpResponseRedirect(reverse(self.redirect_to, args=(movie.id, )))
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
    redirect_to = 'movies:movie-detail'
    info_message = 'You cannot review movie while you are not authenticated'


class RateMovieView(ReviewRateMovieBaseClass):
    form_class = RateMovieForm
    template_name = 'movies/rate_movie.html'
    success_message = 'You successfully rated a movie'
    redirect_to = 'movies:movie-detail'
    info_message = 'You cannot rate movie while you are not authenticated'
