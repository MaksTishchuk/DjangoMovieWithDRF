from django.urls import path
from .views import MovieListView, MovieDetailView, ReviewCreateView, AddStarRatingView

urlpatterns = [
    path('movie/', MovieListView.as_view()),
    path('movie/<int:pk>/', MovieDetailView.as_view()),
    path('review/', ReviewCreateView.as_view()),
    path('rating/', AddStarRatingView.as_view()),
]
