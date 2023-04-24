from django.db import models


class Movie(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    genre = models.CharField(max_length=255)
    release = models.DateField()
    poster = models.ImageField(
        upload_to='cookie/images/movies/', null=False
    )

    def __str__(self):
        return self.title
