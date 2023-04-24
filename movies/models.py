from django.db import models


class Movie(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    release = models.DateField()
    genre = models.ForeignKey('movies.Genre', on_delete=models.CASCADE)
    poster = models.ImageField(
        upload_to='cookie/images/movies/', null=False
    )

    def __str__(self):
        return self.title


class Genre(models.Model):
    title = models.CharField(max_length=255)

    def __str__(self):
        return self.title
