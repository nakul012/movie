from django.urls import path
from .views import (MovieListView, MovieDataListView, MovieCreateFormView, MovieSuccessView,
                    MovieApiListView, ActorApiListView,
                    GenreApiListView, DirectorApiListView
                    )


urlpatterns = [
    path('movie/', MovieListView.as_view()),
    path('create-movie/', MovieCreateFormView.as_view()),
    path('fetch-movie-data/', MovieDataListView.as_view()),
    path('movie-success/', MovieSuccessView.as_view()),
    path('api/movie/', MovieApiListView.as_view()),
    path('api/movie/<pk>/', MovieApiListView.as_view()),
    path('api/actor/', ActorApiListView.as_view()),
    path('api/actor/<pk>/', ActorApiListView.as_view()),
    path('api/genre/', GenreApiListView.as_view()),
    path('api/genre/<pk>/', GenreApiListView.as_view()),
    path('api/director/', DirectorApiListView.as_view()),
    path('api/director/<pk>/', DirectorApiListView.as_view()),

]
