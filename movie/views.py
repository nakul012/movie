from django.shortcuts import render
from .models import Movie, Actor, Director, Genre
from .serializers import (
    MovieSerializer, ActorSerializer, DirectorSerializer, GenreSerializer
)
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from rest_framework.views import APIView
from rest_framework import mixins, generics
from django.shortcuts import get_object_or_404
from rest_framework import generics, status
from django.core.exceptions import ObjectDoesNotExist
from rest_framework.response import Response
from rest_framework.views import APIView
from django.conf import settings
import requests
from django.views.generic import CreateView
from .forms import MovieCreateForm
from rest_framework.renderers import TemplateHTMLRenderer
from rest_framework.views import APIView
from django.http import HttpResponse
from django.shortcuts import render
from django.template import loader


class MovieApiListView(generics.GenericAPIView, mixins.ListModelMixin, mixins.UpdateModelMixin, mixins.DestroyModelMixin):
    serializer_class = MovieSerializer
    queryset = Movie.objects.all()

    def get(self, request, *args, **kwargs):
        if not "pk" in kwargs:
            return self.list(request)
        obj = get_object_or_404(Movie, pk=kwargs["pk"])
        return Response(MovieSerializer(obj).data, status=200)

    def put(self, request, pk=None):
        return self.update(request, pk)

    def delete(self, request, pk=None):
        return self.destroy(request, pk)

    def post(self, request):
        data = request.data
        serializer = MovieSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)


class DirectorApiListView(generics.GenericAPIView, mixins.ListModelMixin, mixins.UpdateModelMixin, mixins.DestroyModelMixin):
    serializer_class = DirectorSerializer
    queryset = Director.objects.all()

    def get(self, request, *args, **kwargs):
        if not "pk" in kwargs:
            return self.list(request)
        obj = get_object_or_404(Director, pk=kwargs["pk"])
        return Response(DirectorSerializer(obj).data, status=200)

    def put(self, request, pk=None):
        return self.update(request, pk)

    def delete(self, request, pk=None):
        return self.destroy(request, pk)

    def post(self, request):
        data = request.data
        serializer = DirectorSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)


class ActorApiListView(generics.GenericAPIView, mixins.ListModelMixin, mixins.UpdateModelMixin, mixins.DestroyModelMixin):
    serializer_class = ActorSerializer
    queryset = Actor.objects.all()

    def get(self, request, *args, **kwargs):
        if not "pk" in kwargs:
            return self.list(request)
        obj = get_object_or_404(Actor, pk=kwargs["pk"])
        return Response(ActorSerializer(obj).data, status=200)

    def put(self, request, pk=None):
        return self.update(request, pk)

    def delete(self, request, pk=None):
        return self.destroy(request, pk)

    def post(self, request):
        data = request.data
        serializer = ActorSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)


class GenreApiListView(generics.GenericAPIView, mixins.ListModelMixin, mixins.UpdateModelMixin, mixins.DestroyModelMixin):
    serializer_class = GenreSerializer
    queryset = Genre.objects.all()

    def get(self, request, *args, **kwargs):
        if not "pk" in kwargs:
            return self.list(request)
        obj = get_object_or_404(Genre, pk=kwargs["pk"])
        return Response(GenreSerializer(obj).data, status=200)

    def put(self, request, pk=None):
        return self.update(request, pk)

    def delete(self, request, pk=None):
        return self.destroy(request, pk)

    def post(self, request):
        data = request.data
        serializer = GenreSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)


class MovieListView(generics.GenericAPIView, mixins.ListModelMixin, mixins.UpdateModelMixin, mixins.DestroyModelMixin):
    serializer_class = MovieSerializer
    queryset = Movie.objects.all()
    renderer_classes = [TemplateHTMLRenderer]

    def get(self, request, *args, **kwargs):
        return Response({'movies': self.get_queryset()}, template_name='home_page.html')

    def get_queryset(self):
        queryset = Movie.objects.all()
        name = self.request.query_params.get('name')
        director = self.request.query_params.get('director')
        cast = self.request.query_params.get('actor')
        genre = self.request.query_params.get('genre')

        if name is not None:
            queryset = Movie.objects.filter(name__icontains=name)
        elif director is not None:
            queryset = Movie.objects.none()
            director_queryset = Director.objects.filter(
                name__icontains=director)
            director_obj_list = list(director_queryset)
            for obj in director_obj_list:
                for m in obj.director.all():
                    movie_queryset = Movie.objects.filter(name=m.name)
                    queryset = queryset.union(movie_queryset)
        elif cast is not None:
            queryset = Actor.objects.none()
            actor_queryset = Actor.objects.filter(name__icontains=cast)
            actor_obj_list = list(actor_queryset)
            for obj in actor_obj_list:
                for m in obj.actor.all():
                    movie_queryset = Movie.objects.filter(name=m.name)
                    queryset = queryset.union(movie_queryset)
        elif genre is not None:
            queryset = Actor.objects.none()
            genre_queryset = Genre.objects.filter(name__icontains=genre)
            genre_obj_list = list(genre_queryset)
            for obj in genre_obj_list:
                for m in obj.genre.all():
                    movie_queryset = Movie.objects.filter(name=m.name)
                    queryset = queryset.union(movie_queryset)
        return queryset


class MovieDataListView(APIView):

    def get(self, request):
        params = request.query_params
        title = params.get("title")
        if not title:
            return Response({
                "error": "title is not provided"
            }, status=400)
        url = f'{settings.OMDB_URL}/?apikey={settings.OMDB_API_KEY}&t={title}'
        x = requests.get(url)
        res = x.json()
        if not x.status_code == 200:
            return Response({
                "error": "server error"
            }, status=500)
        template = loader.get_template('movie_info.html')
        context = {
            'info': res,
        }
        return HttpResponse(template.render(context, request))


class MovieCreateFormView(CreateView):
    template_name = 'create_movie.html'
    form_class = MovieCreateForm
    success_url = '/movie/'
    model = Movie

    def post(self, request, *args, **kwargs):

        form = MovieCreateForm(request.POST)
        template = loader.get_template('movie_success.html')
        if form.is_valid():
            super().post(request, *args, **kwargs)
            context = {
                'message': 'Movie Successfully Added to the Database!'
            }

            return HttpResponse(template.render(context, request))

        context = {
            'message': 'Form is Invalid. Fill the form correctly.'
        }

        return HttpResponse(template.render(context, request))


class MovieSuccessView(APIView):

    def get(self, request):
        params = request.query_params
        title = params.get("title")
        template = loader.get_template('movie_success.html')
        if not title:
            context = {
                'message': 'Title missing!'
            }
            return HttpResponse(template.render(context, request))
        url = f'{settings.OMDB_URL}/?apikey={settings.OMDB_API_KEY}&t={title}'
        x = requests.get(url)
        res = x.json()
        if not x.status_code == 200:
            context = {
                'message': ' OMdb Server error'
            }
            return HttpResponse(template.render(context, request))

        actors = res["Actors"]
        actor_list = actors.split(',')
        director = res["Director"]
        director_list = director.split(",")
        genre = res["Genre"]
        genre_list = genre.split(",")
        title = res["Title"]
        thumbnail_url = res["Poster"]
        released = res["Released"]
        imdb_url = 'https://www.imdb.com/title/' + res["imdbID"]
        imdb_rating = res["imdbRating"]
        movie = Movie.objects.create(
            name=title, thumbnail_url=thumbnail_url, release_date=released, imdb_url=imdb_url, imdb_rating=imdb_rating)
        for actor in actor_list:
            movie.actor.create(name=actor)
        for director in director_list:
            movie.director.create(name=director)
        for genre in genre_list:
            movie.genre.create(name=genre)

        context = {
            'message': 'Movie Successfully Added!'
        }
        return HttpResponse(template.render(context, request))
