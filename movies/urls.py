from django.views.generic import TemplateView
from django.urls import path
from movies import views


app_name = 'movies'
urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('become_user/', TemplateView.
         as_view(template_name='movies/become_user.html'), name='become-user'),
    path('movies/genres/<str:genre>/',
         views.MoviesByGenre.as_view(), name='movies-by-genre'),
    path('movies/<int:pk>/', views.MovieDetailView.as_view(), name='movie-detail'),
    path('movies/<int:pk>/rate/', views.RateMovieView.as_view(), name='rate-movie'),
    path('movies/<int:pk>/rating/update',
         views.UpdateMovieRatingView.as_view(), name='update-rating'),
    path('movies/<int:pk>/rate/delete',
         views.DeleteMovieRatingView.as_view(), name='delete-rating'),
    path('movies/<int:pk>/reviews/',
         views.ReviewsByMovieList.as_view(), name='movie-reviews'),
    path('movies/<int:pk>/review/',
         views.ReviewMovieView.as_view(), name='review-movie'),
    path('movies/<int:pk>/review/update',
         views.UpdateMovieReviewView.as_view(), name='update-review'),
    path('movies/<int:pk>/review/delete',
         views.DeleteMovieReviewView.as_view(), name='delete-review'),
    path('movies/search/', views.search_movies, name='search-movies'),

]
