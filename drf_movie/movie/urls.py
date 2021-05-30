from django.urls import path
from .views import MovieListView, MovieDetailView, ReviewCreateView

urlpatterns = [
    path('movie/', MovieListView.as_view()),
    path('movie/<int:pk>/', MovieDetailView.as_view()),
    path('review/', ReviewCreateView.as_view()),
]
