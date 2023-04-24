from django.db import models
from django.utils.translation import gettext_lazy as _
from taggit.managers import TaggableManager


class Movie(models.Model):
    UNITED_STATES = 'US'
    ENGLAND = 'EN'
    POLAND = 'PL'
    CANADA = 'CA'
    COUNTRIES = (
        (UNITED_STATES, 'United States'),
        (ENGLAND, 'England'),
        (POLAND, 'Poland'),
        (CANADA, 'Canada')
    )
    title = models.CharField(max_length=255)
    synopsis = models.TextField()
    release_date = models.DateField()
    country = models.CharField(max_length=2, choices=COUNTRIES)
    genres = TaggableManager(verbose_name='genres')
    poster = models.ImageField(upload_to='cookie/images/movies/', null=False)
