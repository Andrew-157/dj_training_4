from django.urls import path
from movies import views

urlpatterns = [
    path('movies/', views.MovieListView.as_view())
]
