from django.db import models
from .actor import Actor


class Movie(models.Model):
    name = models.CharField(max_length=155, blank=False, null=False)
    year = models.DateField(blank=False, null=False)
    imdb = models.IntegerField(blank=False, null=False)
    genre = models.CharField(max_length=155, blank=False, null=False)
    actors = models.ManyToManyField(Actor)
