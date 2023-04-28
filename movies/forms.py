from django import forms
from movies.models import Rating, Review


class RateMovieForm(forms.ModelForm):
    class Meta:
        model = Rating
        fields = ['rating']


class ReviewMovieForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ['content']
