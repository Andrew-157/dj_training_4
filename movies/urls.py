from django.urls import path
from movies import views


app_name = 'movies'
urlpatterns = [
    path('movies/genres/<str:genre>/',
         views.MoviesByGenre.as_view(), name='movies-by-genre'),
    path('movies/<int:pk>/', views.MovieDetailView.as_view(), name='movie-detail')
]
