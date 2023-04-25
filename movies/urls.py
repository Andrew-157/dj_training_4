from django.urls import path
from movies import views

urlpatterns = [
    path('movies/<str:genre>/', views.MovieListView.as_view(), name='movie-list')
]
