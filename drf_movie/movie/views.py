from rest_framework import generics, permissions, viewsets
from django.db import models
from django_filters.rest_framework import DjangoFilterBackend
from .models import Movie, Actor
from .serializers import (
    MovieListSerializer,
    MovieDetailSerializer,
    ReviewCreateSerializer,
    CreateRatingSerializer,
    ActorListSerializer,
    ActorDetailSerializer
)
from .service import get_client_ip, MovieFilter, PaginationMovies, PaginationActors


class MovieViewSet(viewsets.ReadOnlyModelViewSet):
    """Вывод списка фильмов"""
    filter_backends = (DjangoFilterBackend,)
    filterset_class = MovieFilter
    pagination_class = PaginationMovies

    def get_queryset(self):
        movies = Movie.objects.filter(draft=False).annotate(
            rating_user=models.Count(
                'ratings',
                filter=models.Q(ratings__ip=get_client_ip(self.request)))
        ).annotate(middle_star=models.Avg("ratings__star"))
        return movies

    def get_serializer_class(self):
        if self.action == 'list':
            return MovieListSerializer
        elif self.action == "retrieve":
            return MovieDetailSerializer


class ReviewCreateViewSet(viewsets.ModelViewSet):
    """Добавление отзыва к фильму"""
    serializer_class = ReviewCreateSerializer


class AddStarRatingViewSet(viewsets.ModelViewSet):
    """Добавление рейтинга фильму"""
    serializer_class = CreateRatingSerializer

    def perform_create(self, serializer):
        serializer.save(ip=get_client_ip(self.request))


class ActorsViewSet(viewsets.ReadOnlyModelViewSet):
    """Вывод актеров или режиссеров"""
    queryset = Actor.objects.all()
    pagination_class = PaginationActors

    def get_serializer_class(self):
        if self.action == 'list':
            return ActorListSerializer
        elif self.action == "retrieve":
            return ActorDetailSerializer


# class MovieListView(generics.ListAPIView):
#     """Вывод списка фильмов. Информация о среднем значении рейтинга фильма и о том, установил ли
#     рейтинг данный пользователь"""
#
#     serializer_class = MovieListSerializer
#     filter_backends = (DjangoFilterBackend,)
#     filterset_class = MovieFilter
#
#     def get_queryset(self):
#         movies = Movie.objects.filter(draft=False).annotate(
#             rating_user=models.Count(
#                 'ratings',
#                 filter=models.Q(ratings__ip=get_client_ip(self.request)))
#         ).annotate(middle_star=models.Avg("ratings__star"))
#         return movies
#
#
# class MovieDetailView(generics.RetrieveAPIView):
#     """Вывод полной информации о фильме"""
#
#     queryset = Movie.objects.filter(draft=False)
#     serializer_class = MovieDetailSerializer
#
#
# class ReviewCreateView(generics.CreateAPIView):
#     """Добавление отзыва к фильму"""
#
#     serializer_class = ReviewCreateSerializer
#
#
# class AddStarRatingView(generics.CreateAPIView):
#     """Добавление рейтинга к фильму"""
#
#     serializer_class = CreateRatingSerializer
#
#     def perform_create(self, serializer):
#         serializer.save(ip=get_client_ip(self.request))
#
#
# class ActorsListView(generics.ListAPIView):
#     """Вывод списка актеров/режиссеров"""
#
#     queryset = Actor.objects.all()
#     serializer_class = ActorListSerializer
#
#
# class ActorsDetailView(generics.RetrieveAPIView):
#     """Вывод детальной информации про актера/режисера"""
#
#     queryset = Actor.objects.all()
#     serializer_class = ActorDetailSerializer
