from django.views.generic import TemplateView
from django.urls import path
from movies import views


app_name = 'movies'
urlpatterns = [
    path('', TemplateView.as_view(
        template_name='movies/index.html'), name='index'),
    path('become_user/', TemplateView.
         as_view(template_name='movies/become_user.html'), name='become-user'),
    path('movies/genres/<str:genre>/',
         views.MoviesByGenre.as_view(), name='movies-by-genre'),
    path('movies/<int:pk>/', views.MovieDetailView.as_view(), name='movie-detail'),
    path('movies/<int:pk>/rate/', views.RateMovieView.as_view(), name='rate-movie'),
    path('movies/<int:pk>/review/',
         views.ReviewMovieView.as_view(), name='review-movie')
]
