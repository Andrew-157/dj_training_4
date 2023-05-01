from typing import Any, Dict
from django.db.models import Avg
from django.db.models.query_utils import Q
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.utils.decorators import method_decorator
from django.shortcuts import render, redirect
from django.views.generic import ListView, DetailView
from django.views import View
from django.views.generic.edit import UpdateView
from taggit.models import Tag
from movies.models import Movie, Review, Rating
from movies.forms import RateMovieForm, ReviewMovieForm


class MoviesByGenre(ListView):
    model = Movie
    context_object_name = 'movies'
    template_name = "movies/movies_by_genre.html"

    def get_queryset(self):
        genre = self.kwargs['genre']
        genre_object = Tag.objects.filter(slug=genre).first()
        movies = Movie.objects.prefetch_related(
            'genres').filter(genres=genre_object).\
            order_by('-release_date').all().\
            annotate(avg_rating=Avg('rating__rating'))
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
    user_has_review = False

    def get_queryset(self):
        pk = self.kwargs['pk']
        movie = Movie.objects.filter(pk=pk).first()
        # return nonexistent.html if no movie with this pk
        if not movie:
            self.valid_movie_pk = False
            self.template_name = 'movies/nonexistent.html'
            return None
        # find all reviews about the movie
        reviews = Review.objects.select_related('owner').\
            order_by('-pub_date').filter(movie=movie).all()
        # find all ids of users that left review on the movie
        # to check if current user already has a review
        review_owner_ids = [review.owner.id for review in reviews]
        current_user = self.request.user
        if current_user.is_authenticated and current_user.id in review_owner_ids:
            # if user has a review change self.user_has_review to True for further usage
            self.user_has_review = True
        self.kwargs['movie'] = movie
        return reviews

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # variable valid_movie_pk lets us know if pk provided in url is valid
        # if it is not, then we return context as it was because we are gonna show
        # that the resource does not exist
        if not self.valid_movie_pk:
            return context
        else:
            context['movie'] = self.kwargs['movie']
            context['user_has_review'] = self.user_has_review
            return context


class MovieDetailView(DetailView):
    model = Movie
    template_name = 'movies/movie_detail.html'
    queryset = Movie.objects.prefetch_related('genres').all().\
        annotate(avg_rating=Avg('rating__rating'))
    context_object_name = 'movie'

    def get_object(self):
        movie_pk = self.kwargs['pk']
        movie = Movie.objects.filter(pk=movie_pk).first()
        if not movie:
            self.template_name = 'movies/nonexistent.html'
            return None
        return super().get_object()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        current_user = self.request.user
        movie_pk = self.kwargs['pk']
        if current_user.is_authenticated:
            rating_by_user = Rating.objects.filter(
                Q(owner=current_user) &
                Q(movie__pk=movie_pk)
            ).first()
            if rating_by_user:
                context['rating_by_user'] = rating_by_user.rating
            else:
                context['rating_by_user'] = None
        else:
            context['rating_by_user'] = None
        return context


class ReviewRateMovieBaseClass(View):
    form_class = None
    template_name = ''
    success_message = ''
    info_message = ''
    warning_message = ''
    nonexistent_template = 'movies/nonexistent.html'
    redirect_to = ''
    model = None

    def exists(self, owner, pk):
        model = self.model
        return model.objects.filter(
            Q(owner=owner) &
            Q(movie__pk=pk)
        ).first()

    def get_object(self, pk):
        obj = Movie.objects.filter(pk=pk).first()
        return obj

    def get(self, request, *args, **kwargs):
        current_user = request.user
        movie = self.get_object(self.kwargs['pk'])
        # if no movie with this id return nonexistent.html
        if not movie:
            return render(request, self.nonexistent_template)
        # if user is not authenticated they cannot neither rate movie nor review it
        if not current_user.is_authenticated:
            messages.info(request, self.info_message)
            return HttpResponseRedirect(reverse(self.redirect_to, args=(movie.id, )))
        # if user already has a review or rating of a movie
        # and tries to hit urls for rating or reviewing,
        # we return a warning that they can only change their review or rating
        if self.exists(current_user, movie.pk):
            messages.warning(request, self.warning_message)
            return HttpResponseRedirect(reverse(self.redirect_to, args=(movie.id, )))
        form = self.form_class()
        return render(request, self.template_name, {'form': form, 'movie': movie})

    def post(self, request, **kwargs):
        current_user = request.user
        movie = self.get_object(kwargs['pk'])
        form = self.form_class(request.POST)
        if form.is_valid():
            form.instance.movie = movie
            form.instance.owner = current_user
            form.save()
            messages.success(request, self.success_message)
            return HttpResponseRedirect(reverse(self.redirect_to, args=(kwargs['pk'], )))
        return render(request, self.template_name, {'form': form, 'movie': movie})


class UpdateRateReviewMovieBaseClass(View):
    form_class = None
    template_name = ''
    nonexistent_template = 'movies/nonexistent.html'
    redirect_to = ''
    warning_message = ''
    success_message = ''
    model = ''

    def get_movie(self, pk):
        return Movie.objects.filter(pk=pk).first()

    def exists(self, owner, pk):
        model = self.model
        return model.objects.filter(
            Q(owner=owner) &
            Q(movie__pk=pk)
        ).first()

    def get(self, request, *args, **kwargs):
        current_user = request.user
        movie = self.get_movie(self.kwargs['pk'])
        if not movie:
            return render(request, self.nonexistent_template)
        obj = self.exists(current_user, movie.id)
        if not obj:
            messages.warning(request, self.warning_message)
            return HttpResponseRedirect(reverse(self.redirect_to, args=(movie.id, )))
        form = self.form_class(instance=obj)
        return render(request, self.template_name, {'form': form, 'movie': movie})

    def post(self, request, **kwargs):
        current_user = request.user
        movie = self.get_movie(kwargs['pk'])
        obj = self.exists(current_user, movie.id)
        form = self.form_class(request.POST, instance=obj)
        if form.is_valid():
            form.save()
            messages.success(request, self.success_message)
            return HttpResponseRedirect(reverse(self.redirect_to, args=(self.kwargs['pk'], )))
        return render(request, self.template_name, {'form': form, 'movie': movie})

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)


class UpdateReviewMovieView(UpdateRateReviewMovieBaseClass):
    form_class = ReviewMovieForm
    template_name = 'movies/update_review.html'
    redirect_to = 'movies:movie-reviews'
    success_message = 'You successfully updated your review on this movie'
    warning_message = 'You have not reviewed this movie yet, you cannot update your review'
    model = Review


class UpdateRateMovieView(UpdateRateReviewMovieBaseClass):
    form_class = RateMovieForm
    template_name = 'movies/update_rating.html'
    redirect_to = 'movies:movie-detail'
    success_message = 'You successfully updated your rating of this movie'
    warning_message = 'You have not rated this movie yet, you cannot update your rating'
    model = Rating


class ReviewMovieView(ReviewRateMovieBaseClass):
    form_class = ReviewMovieForm
    template_name = 'movies/review_movie.html'
    success_message = 'You successfully reviewed a movie'
    redirect_to = 'movies:movie-reviews'
    info_message = 'You cannot review movie while you are not authenticated'
    warning_message = 'You can only change your existing review of a movie, not write a new one'
    model = Review


class RateMovieView(ReviewRateMovieBaseClass):
    form_class = RateMovieForm
    template_name = 'movies/rate_movie.html'
    success_message = 'You successfully rated a movie'
    redirect_to = 'movies:movie-detail'
    info_message = 'You cannot rate movie while you are not authenticated'
    warning_message = 'You can only change your rate of a movie, not add a new one'
    model = Rating


def search_movies(request):
    search_string = request.POST['search_string']
    if not search_string:
        return render(request, 'movies/nonexistent.html')
    movies = Movie.objects.\
        prefetch_related('genres').\
        filter(Q(title__icontains=search_string)).\
        order_by('-release_date').all().\
        annotate(avg_rating=Avg('rating__rating'))
    return render(request, 'movies/search_movies.html', {'movies': movies,
                                                         'search_string': search_string})


class IndexView(ListView):
    model = Tag
    context_object_name = 'genres'
    template_name = 'movies/index.html'
    queryset = Tag.objects.order_by('name').all()
