from django.core.exceptions import ValidationError
from django.db import models
from django.utils.translation import gettext_lazy as _
from taggit.managers import TaggableManager


def validate_image(image):
    file_size = image.file.size
    limit_kb = 150
    if file_size > limit_kb * 1024:
        raise ValidationError(f"Maximum size of the image is {limit_kb} KB")

    # file_size = image.file.size
    # limit_mb = 8
    # if file_size > limit_mb * 1024 * 1024:
    #     raise ValidationError(f"Maximum size of the image is {limit_mb} MB")


class Movie(models.Model):
    UNITED_STATES = 'US'
    UNITED_KINGDOM = 'UK'
    POLAND = 'PL'
    CANADA = 'CA'
    COUNTRIES = (
        (UNITED_STATES, 'United States'),
        (UNITED_KINGDOM, 'United Kingdom'),
        (POLAND, 'Poland'),
        (CANADA, 'Canada')
    )
    title = models.CharField(max_length=255)
    synopsis = models.TextField()
    release_date = models.DateField()
    country = models.CharField(max_length=2, choices=COUNTRIES)
    genres = TaggableManager(verbose_name='genres',
                             help_text='A comma-separated list of genres.')
    poster = models.ImageField(
        upload_to='cookie/images/movies/', null=False, validators=[validate_image])

    def __str__(self):
        return self.title


class Rating(models.Model):
    rating_choices = [(0, 0), (1, 1), (2, 2), (3, 3), (4, 4), (5, 5),
                      (6, 6), (7, 7), (8, 8), (9, 9), (10, 10)]
    rating = models.PositiveSmallIntegerField(choices=rating_choices)
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE)
    owner = models.ForeignKey('auth.User', on_delete=models.CASCADE)


class Review(models.Model):
    content = models.TextField()
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE)
    owner = models.ForeignKey('auth.User', on_delete=models.CASCADE)
    pub_date = models.DateTimeField(auto_now=True)
