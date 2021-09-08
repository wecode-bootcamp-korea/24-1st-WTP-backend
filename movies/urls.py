from django.urls  import path

from movies.views import RateView, GenreMovieView, MovieView, MovieDetailView, CommentView, UserRateView

urlpatterns = [
    path("",MovieView.as_view()),
    path('/<int:movie_id>', MovieDetailView.as_view()),
    path('/rate/<int:movie_id>', RateView.as_view()),
    path('/related_movies', GenreMovieView.as_view()),
    path("/<int:movie_id>/comments",CommentView.as_view()),
    path('/<int:movie_id>/rate', UserRateView.as_view())
]
