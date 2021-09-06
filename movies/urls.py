from django.urls import path

from movies.views import MovieView, RatingView

urlpatterns = [
    path("movie",MovieView.as_view()),
]