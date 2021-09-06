from django.urls import path, include

from movies.views import RateUpdate, RelatedMovie
from users.views import Login


urlpatterns = [
    path('/<int:movie_id>/rate', RateUpdate.as_view()),
    path('/<int:movie_id>/related_movies', RelatedMovie.as_view()),
]

