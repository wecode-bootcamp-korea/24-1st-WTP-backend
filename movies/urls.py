from django.urls import path, include

from movies.views import RateUpdate
from users.views import Login


urlpatterns = [
    path('/<int:movie_id>/rate', RateUpdate.as_view()),
]

