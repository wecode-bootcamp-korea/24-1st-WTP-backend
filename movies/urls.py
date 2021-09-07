from django.urls import path

from movies.views import RateUpdate, RelatedMovie
from users.views import Login
from django.urls import path

from movies.views import MovieView

urlpatterns = [
    path("",MovieView.as_view()),
    path('/rate/<int:movie_id>', RateUpdate.as_view()),
    path('/related_movies', RelatedMovie.as_view()),
]

