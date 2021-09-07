from django.urls import path, include

from movies.views import RateUpdate, RelatedMovie
from users.views import Login


urlpatterns = [
    path('/rate/<int:movie_id>', RateUpdate.as_view()),
    path('/related_movies', RelatedMovie.as_view()),
]

