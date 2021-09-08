from django.urls  import path

from movies.views import MovieView, MovieDetailView, SearchView

urlpatterns = [
    path("",MovieView.as_view()),
    path('/<int:movie_id>', MovieDetailView.as_view()),
    path('/search', SearchView.as_view()),
    ]
