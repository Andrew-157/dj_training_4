from django.urls import path
from movies import views


app_name = 'movies'
urlpatterns = [
    path('movies/genres/<str:genre>/',
         views.MovieListView.as_view(), name='movie-list'),
    path('movies/<int:pk>/', views.MovieDetailView.as_view(), name='movie-detail')
]
