from django.urls import path

from movies.views import MovieView

urlpatterns = [
    path("movie",MovieView.as_view()),
]