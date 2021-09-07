from django.urls import path

from movies.views import RateView, GenreMovieView
from users.views import Login
from django.urls import path

from movies.views import MovieView

urlpatterns = [
    path("",MovieView.as_view()),
    path('/rate/<int:movie_id>', RateView.as_view()),
    path('/related_movies', GenreMovieView.as_view()),
]

