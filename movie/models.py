from django.shortcuts import render
from django.db import models
from django.contrib import admin


class Actor(models.Model):
    name = models.CharField(max_length=100)
    nationality = models.CharField(max_length=100, blank=True, null=True)

    def __str__(self) -> str:
        return self.name


class Director(models.Model):
    name = models.CharField(max_length=100)
    nationality = models.CharField(max_length=100, blank=True, null=True)

    def __str__(self) -> str:
        return self.name


class Genre(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self) -> str:
        return self.name


class Movie(models.Model):
    name = models.CharField(max_length=100)
    actor = models.ManyToManyField(Actor, related_name="actor")
    director = models.ManyToManyField(Director, related_name="director")
    genre = models.ManyToManyField(Genre, related_name="genre")
    release_date = models.CharField(max_length=100, null=True, blank=True)
    imdb_rating = models.CharField(max_length=10,  null=True, blank=True)
    imdb_url = models.CharField(max_length=200, unique=True)
    thumbnail_url = models.CharField(max_length=200, null=True, blank=True)

    def __str__(self) -> str:
        return self.name


admin.site.register(Movie)
admin.site.register(Actor)
admin.site.register(Director)
admin.site.register(Genre)
