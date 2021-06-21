from django.urls import path
# from .views import (
#     MovieListView,
#     MovieDetailView,
#     ReviewCreateView,
#     AddStarRatingView,
#     ActorsListView,
#     ActorsDetailView
# )
from rest_framework.routers import DefaultRouter
from rest_framework.urlpatterns import format_suffix_patterns

from . import views

urlpatterns = format_suffix_patterns([
    path("movies/", views.MovieViewSet.as_view({'get': 'list'})),
    path("movies/<int:pk>/", views.MovieViewSet.as_view({'get': 'retrieve'})),
    path("review/", views.ReviewCreateViewSet.as_view({'post': 'create'})),
    path("rating/", views.AddStarRatingViewSet.as_view({'post': 'create'})),
    path('actors/', views.ActorsViewSet.as_view({'get': 'list'})),
    path('actors/<int:pk>/', views.ActorsViewSet.as_view({'get': 'retrieve'})),
])

# urlpatterns = [
#     path('movie/', MovieListView.as_view()),
#     path('movie/<int:pk>/', MovieDetailView.as_view()),
#     path('review/', ReviewCreateView.as_view()),
#     path('rating/', AddStarRatingView.as_view()),
#     path('actors/', ActorsListView.as_view()),
#     path('actors/<int:pk>', ActorsDetailView.as_view()),
# ]
