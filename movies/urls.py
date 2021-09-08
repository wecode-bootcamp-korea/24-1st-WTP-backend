from django.urls  import path

from movies.views import MovieView, CommentView, MovieDetailView   

urlpatterns = [
    path("",MovieView.as_view()),
    path('/<int:movie_id>', MovieDetailView.as_view()),
    path("/<int:movie_id>/comments",CommentView.as_view())
]