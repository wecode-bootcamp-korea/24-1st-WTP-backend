from django.urls  import path

from movies.views import MovieView, MovieDetailView

urlpatterns = [
    path("",MovieView.as_view()),
    path('/<int:movie_id>', MovieDetailView.as_view()),
    ]
