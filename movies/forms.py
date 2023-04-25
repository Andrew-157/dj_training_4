from django import forms
from movies.models import Rating


class RateMovieForm(forms.ModelForm):
    class Meta:
        model = Rating
        fields = ['rating']
